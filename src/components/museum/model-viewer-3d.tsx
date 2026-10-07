"use client";

import { useEffect } from "react";
import { Box } from "lucide-react";
import { useLang } from "./language-context";

/**
 * Prikaz interpretativnega 3D-modela zapisa (GLB) prek <model-viewer>.
 * Knjižnico naložimo dinamično (ločen chunk) — samo kadar zapis dejansko ima model.
 */
export function ModelViewer3D({
  src,
  credit,
}: {
  src: string;
  credit?: string | null;
}) {
  const { t } = useLang();

  useEffect(() => {
    // stranski uvoz: registrira <model-viewer> custom element
    import("@google/model-viewer").catch((err) => {
      console.error("model-viewer load failed", err);
    });
  }, []);

  return (
    <section className="mt-6" aria-labelledby="model3d-naslov">
      <h2
        id="model3d-naslov"
        className="flex items-center gap-2 font-display text-xl font-semibold"
      >
        <Box className="size-5 text-primary" aria-hidden="true" />
        {t("Prostornina — interpretativni 3D-model", "Volume — interpretive 3D model")}
      </h2>
      <p className="mt-1 text-xs text-muted-foreground">
        {t(
          "Zavrtite s prstom ali miško; približajte s koleščkom ali ščepom. Na telefonu: Postavi v prostor — Android (WebXR) ali iPhone (AR Quick Look).",
          "Drag to orbit; scroll or pinch to zoom. On your phone: place it in your space — Android (WebXR) or iPhone (AR Quick Look).",
        )}
      </p>
      <div className="mt-3 overflow-hidden rounded-xl border bg-secondary/40">
        <model-viewer
          src={src}
          /* dual model (issue #12): Android/WebXR → GLB, iPhone → USDZ Quick Look */
          ios-src={src.replace(/\.glb$/, ".usdz")}
          alt={t(
            "Interpretativni 3D-model: cerkev sv. Vida v Gribljah",
            "Interpretive 3D model: the church of St. Vid in Griblje",
          )}
          camera-controls
          auto-rotate
          rotation-per-second="18deg"
          shadow-intensity="0.7"
          shadow-softness="0.8"
          exposure="1.05"
          camera-orbit="-35deg 68deg auto"
          max-field-of-view="45deg"
          interaction-prompt="auto"
          ar
          ar-modes="webxr scene-viewer quick-look"
          ar-placement="floor"
          ar-scale="auto"
          className="block h-[340px] w-full sm:h-[400px] [&::part(default-progress-bar)]:hidden"
        >
          <div
            slot="progress-bar"
            className="mx-auto mt-40 w-32 text-center text-xs text-muted-foreground"
          >
            {t("Nalaganje modela …", "Loading model …")}
          </div>
        </model-viewer>
      </div>
      {credit && (
        <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground">
          {credit}
        </p>
      )}
    </section>
  );
}
