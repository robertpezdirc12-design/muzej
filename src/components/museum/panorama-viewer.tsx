"use client";

/**
 * HISTORICAL PANORAMA VIEWER (issue #13 — P2 VISUAL REALISM).
 *
 * TimeLens-style »magic window«: equirectangular 360° slika na notranji
 * strani sfere, kamera v središču. Pogled obračata kompas/žiroskop
 * (useCompass iz #14 — glajenje + kalibracija); vlečenje po zaslonu je
 * fallback brez senzorjev. NE WebXR — isto Three.js okolje kot časovni
 * stroj, isto zajemno geometrijo napisnic.
 *
 * Nalaganje: predogled (~33 KB) takoj, polna slika (~340 KB) v ozadju —
 * lazy, samo AKTIVNI TimeSpot nalozi svojo panoramo; ob izhodu se tekstura
 * in renderer počistijo (dispose).
 *
 * »Primerjaj z danes« = živa kamera (danes je realnost, ne generirana
 * slika): sfera se prelije na prosojnost, telefonu pokaže danes.
 */

import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import type { HistoricalPanorama } from "@/data/atlas/panoramas";

export interface PanoCaptionSpec {
  title: string;
  sub: string;
  credit: string;
}

export type PanoLoadState = "loading" | "preview" | "full" | "error";

/* ── Three.js prizor panorama (razred, kot VillageScene) ── */

export class PanoramaScene {
  private renderer: THREE.WebGLRenderer;
  private scene = new THREE.Scene();
  private camera: THREE.PerspectiveCamera;
  private mesh: THREE.Mesh | null = null;
  private mat: THREE.MeshBasicMaterial | null = null;
  private raf = 0;
  private disposed = false;
  private ro: ResizeObserver;
  private canvas: HTMLCanvasElement;

  /** azimut središča slike (u=0,5) — določen, determinističen začetni pogled */
  private heading0: number;
  /** kompasni azimut uporabnika (deg) ali null (brez senzorja) */
  private compassYaw: number | null = null;
  private manualYaw = 0;
  private manualPitch = 0;
  private curYaw: number;
  private curPitch = 0;
  private todayTarget = 0;
  private todayCur = 0;

  private pointerDown: { x: number; y: number } | null = null;
  private dragging = false;

  constructor(
    canvas: HTMLCanvasElement,
    opts: { headingDeg: number; onLoad?: (s: PanoLoadState) => void },
  ) {
    this.canvas = canvas;
    this.heading0 = opts.headingDeg;
    this.onLoad = opts.onLoad;
    /* deterministični začetni pogled: središče slike (= heading0) */
    this.curYaw = 90;
    this.curPitch = 0;

    this.renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    this.renderer.setClearColor(0x000000, 0);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    this.camera = new THREE.PerspectiveCamera(70, 1, 0.1, 1100);
    this.camera.rotation.order = "YXZ";
    this.camera.position.set(0, 0, 0);

    this.ro = new ResizeObserver(() => this.resize());
    this.ro.observe(canvas);
    this.resize();

    canvas.addEventListener("pointerdown", this.handleDown);
    canvas.addEventListener("pointermove", this.handleMove);
    canvas.addEventListener("pointerup", this.handleUp);
    canvas.addEventListener("pointercancel", this.handleUp);

    this.loop();
  }

  private onLoad?: (s: PanoLoadState) => void;

  /** naloži predogled in (v ozadju) polno sliko — lazy zamenjava */
  async load(previewUrl: string | null, fullUrl: string): Promise<void> {
    const loader = new THREE.TextureLoader();
    loader.setCrossOrigin("anonymous");
    const setTex = (tex: THREE.Texture) => {
      if (this.disposed) {
        tex.dispose();
        return;
      }
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.wrapS = THREE.RepeatWrapping;
      if (!this.mesh) {
        /* obrnjena sfera (three.js equirect recept: scale(-1,1,1)) */
        const geo = new THREE.SphereGeometry(500, 64, 44);
        geo.scale(-1, 1, 1);
        this.mat = new THREE.MeshBasicMaterial({
          map: tex,
          transparent: true,
          opacity: 1,
        });
        this.mesh = new THREE.Mesh(geo, this.mat);
        this.scene.add(this.mesh);
      } else {
        this.mat?.map?.dispose();
        this.mat!.map = tex;
        this.mat!.needsUpdate = true;
      }
    };
    if (previewUrl) {
      try {
        const prev = await loader.loadAsync(previewUrl);
        if (this.disposed) return;
        setTex(prev);
        this.onLoad?.("preview");
      } catch {
        /* predogled ni obvezen — čakamo polno sliko */
      }
    }
    try {
      const full = await loader.loadAsync(fullUrl);
      if (this.disposed) return;
      setTex(full);
      this.onLoad?.("full");
    } catch {
      if (!this.mesh) this.onLoad?.("error");
      else this.onLoad?.("full");
    }
  }

  /** kompas (deg azimut uporabnika) → prizor; null = samo vlečenje */
  setCompassYaw(deg: number | null) {
    this.compassYaw = deg;
  }

  /** vlečenje prstom: zamik pogleda (popravek brez/ob kompasu) */
  nudgeLook(dxPx: number, dyPx: number) {
    const k = 0.12;
    this.manualYaw -= dxPx * k;
    this.manualPitch = THREE.MathUtils.clamp(this.manualPitch - dyPx * k * 0.7, -70, 70);
  }

  /** ponovna poravnava pogleda na kompas (oz. središče slike) */
  realign() {
    this.manualYaw = 0;
    this.manualPitch = 0;
  }

  /** »primerjaj z danes«: sfera se prelije v duha nad živo kamero */
  setTodayBlend(on: boolean) {
    this.todayTarget = on ? 1 : 0;
  }

  capture(video: HTMLVideoElement | null, cap: PanoCaptionSpec): string | null {
    const w = Math.max(640, Math.floor(this.canvas.clientWidth));
    const h = Math.max(480, Math.floor(this.canvas.clientHeight));
    const out = document.createElement("canvas");
    out.width = w;
    out.height = h;
    const ctx = out.getContext("2d");
    if (!ctx) return null;

    /* živa kamera kot ozadje, če je vklopljena (danes-blend) */
    if (video && video.readyState >= 2 && this.todayCur > 0.5) {
      const vw = video.videoWidth, vh = video.videoHeight;
      const scale = Math.max(w / vw, h / vh);
      ctx.drawImage(video, (w - vw * scale) / 2, (h - vh * scale) / 2, vw * scale, vh * scale);
    } else {
      ctx.fillStyle = "#101610";
      ctx.fillRect(0, 0, w, h);
    }

    this.renderer.render(this.scene, this.camera);
    ctx.drawImage(this.renderer.domElement, 0, 0, w, h);

    /* napisnica — isti vzorec kot VillageScene.capture */
    const barH = Math.round(h * 0.115);
    const grad = ctx.createLinearGradient(0, h - barH * 1.6, 0, h);
    grad.addColorStop(0, "rgba(8,12,9,0)");
    grad.addColorStop(0.35, "rgba(8,12,9,0.82)");
    grad.addColorStop(1, "rgba(8,12,9,0.95)");
    ctx.fillStyle = grad;
    ctx.fillRect(0, h - barH * 1.6, w, barH * 1.6);
    ctx.textBaseline = "alphabetic";
    ctx.fillStyle = "#f2eee6";
    ctx.font = `600 ${Math.round(h * 0.034)}px Georgia, 'Times New Roman', serif`;
    ctx.fillText(cap.title, Math.round(w * 0.04), h - barH);
    ctx.fillStyle = "rgba(242,238,230,0.85)";
    ctx.font = `${Math.round(h * 0.022)}px Georgia, serif`;
    ctx.fillText(cap.sub, Math.round(w * 0.04), h - barH * 0.55);
    ctx.fillStyle = "rgba(242,238,230,0.6)";
    ctx.font = `${Math.round(h * 0.02)}px Georgia, serif`;
    ctx.fillText(cap.credit, Math.round(w * 0.04), h - barH * 0.18);

    try {
      return out.toDataURL("image/png");
    } catch {
      return null;
    }
  }

  dispose() {
    this.disposed = true;
    cancelAnimationFrame(this.raf);
    this.ro.disconnect();
    this.canvas.removeEventListener("pointerdown", this.handleDown);
    this.canvas.removeEventListener("pointermove", this.handleMove);
    this.canvas.removeEventListener("pointerup", this.handleUp);
    this.canvas.removeEventListener("pointercancel", this.handleUp);
    this.mat?.map?.dispose();
    this.mesh?.geometry.dispose();
    this.mat?.dispose();
    this.renderer.dispose();
  }

  /* ── notranje ── */

  private handleDown = (e: PointerEvent) => {
    this.pointerDown = { x: e.clientX, y: e.clientY };
    this.dragging = false;
  };

  private handleMove = (e: PointerEvent) => {
    if (!this.pointerDown) return;
    const dx = e.clientX - this.pointerDown.x;
    const dy = e.clientY - this.pointerDown.y;
    if (Math.abs(dx) + Math.abs(dy) > 6) this.dragging = true;
    if (this.dragging) {
      this.nudgeLook(dx, dy);
      this.pointerDown = { x: e.clientX, y: e.clientY };
    }
  };

  private handleUp = () => {
    this.pointerDown = null;
  };

  private resize() {
    const parent = this.canvas.parentElement;
    const w = parent?.clientWidth || this.canvas.clientWidth || 640;
    const h = parent?.clientHeight || this.canvas.clientHeight || 480;
    this.renderer.setSize(w, h, false);
    /* FOV: pokrajinski zaslon ~65°, pokončni telefon širše (70–82°) */
    this.camera.aspect = w / Math.max(1, h);
    this.camera.fov = this.camera.aspect < 0.9 ? 82 : this.camera.aspect < 1.6 ? 72 : 62;
    this.camera.updateProjectionMatrix();
  }

  private loop = () => {
    if (this.disposed) return;
    this.raf = requestAnimationFrame(this.loop);

    /* žiroskop/kompas → yaw; vlečenje doda zamik (mehko, kot AR) */
    const base =
      this.compassYaw != null ? 90 + this.heading0 - this.compassYaw : 90;
    const yawTarget = base + this.manualYaw;
    const pitchTarget = this.manualPitch;
    this.curYaw += (yawTarget - this.curYaw) * 0.18;
    this.curPitch += (pitchTarget - this.curPitch) * 0.18;
    this.camera.rotation.set(
      THREE.MathUtils.degToRad(this.curPitch),
      THREE.MathUtils.degToRad(this.curYaw),
      0,
    );

    /* danes-blend: prosojnost sfere (1825 kot duh nad kamero) */
    this.todayCur += (this.todayTarget - this.todayCur) * 0.1;
    if (this.mat) this.mat.opacity = 1 - this.todayCur * 0.85;

    this.renderer.render(this.scene, this.camera);
  };
}

/* ── React komponenta: canvas + stanje nalaganja ── */

export function PanoramaViewer({
  pano,
  heading,
  onExit,
  sceneRef,
}: {
  pano: HistoricalPanorama;
  /** glajen kompasni azimut (useCompass) ali null */
  heading: number | null;
  onExit: () => void;
  /** komponenta AR časovnega stroja shrani prizor sem (zajem, realign) */
  sceneRef: React.MutableRefObject<PanoramaScene | null>;
}) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [state, setState] = useState<PanoLoadState>("loading");
  const stateRef = useRef<PanoLoadState>("loading");

  /* ref posodobljen v učinku (ne med renderjem — pravilo react-hooks/refs) */
  useEffect(() => {
    stateRef.current = state;
  }, [state]);

  useEffect(() => {
    let cancelled = false;
    let sc: PanoramaScene | null = null;
    try {
      sc = new PanoramaScene(canvasRef.current!, {
        headingDeg: pano.headingDeg,
        onLoad: (s) => {
          if (!cancelled && s !== stateRef.current) setState(s);
        },
      });
    } catch {
      /* WebGL ni na voljo — odloženo (kaskadni render v učinku ni dovoljen) */
      window.setTimeout(() => !cancelled && setState("error"), 0);
      return;
    }
    sceneRef.current = sc;
    void sc.load(pano.previewUrl, pano.imageUrl);
    return () => {
      cancelled = true;
      sc?.dispose();
      sceneRef.current = null;
    };
  }, [pano.id]);

  /* kompas → prizor */
  useEffect(() => {
    sceneRef.current?.setCompassYaw(heading);
  }, [heading, sceneRef]);

  return (
    <>
      <canvas
        ref={canvasRef}
        aria-label={`${pano.titleSi} — 360° zgodovinski pogled; vlecite za obrat`}
        className={`absolute inset-0 h-full w-full touch-none transition-opacity duration-500 ${
          state === "full" || state === "preview" ? "opacity-100" : "opacity-0"
        }`}
      />
      {state === "loading" && (
        <div className="absolute inset-0 flex items-center justify-center" role="status">
          <div className="rounded-xl border border-white/20 bg-black/60 p-4 text-center backdrop-blur">
            <div className="mx-auto size-8 animate-spin rounded-full border-2 border-white/30 border-t-white" />
            <p className="mt-2 text-xs text-white/85">
              {pano.titleSi} — nalagam 360° prizor …
            </p>
            <p className="mt-1 text-[10px] text-white/50">predogled ~33 KB · slika ~340 KB</p>
          </div>
        </div>
      )}
      {state === "error" && (
        <div className="absolute inset-0 flex items-center justify-center p-4">
          <div
            className="max-w-sm rounded-xl border border-red-300/40 bg-black/75 p-4 text-center text-white backdrop-blur"
            role="alert"
          >
            <p className="font-display text-sm font-semibold">
              Panorame ni bilo mogoče naložiti
            </p>
            <p className="mt-1.5 text-xs leading-relaxed text-white/80">
              Omrežje ali WebGL ni na voljo. Proceduralna 3D rekonstrukcija
              ostane kot zanesljiv nadomestek.
            </p>
            <button
              type="button"
              onClick={onExit}
              className="mt-3 rounded-full border border-white/30 bg-white/10 px-4 py-2 text-xs font-semibold transition-colors hover:bg-white/20"
            >
              ← nazaj na 3D rekonstrukcijo
            </button>
          </div>
        </div>
      )}
    </>
  );
}
