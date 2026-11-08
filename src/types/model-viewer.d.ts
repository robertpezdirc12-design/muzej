import type { CSSProperties, DOMAttributes, Ref } from "react";
import type { ModelViewerElement } from "@google/model-viewer";

/** JSX tipi za <model-viewer> (Google, @google/model-viewer) — React 19 podpira custom elemente. */
export type ModelViewerAttributes = DOMAttributes<HTMLElement> & {
  /** referenca na element (npr. za klice activateAR / toSphericalCoordinates) */
  ref?: Ref<ModelViewerElement | null>;
  className?: string;
  style?: CSSProperties;
  id?: string;
  src?: string;
  /** USDZ dvojnik — iOS AR Quick Look (iPhone nima WebXR; vzorec Nîmes GLB+USDZ) */
  "ios-src"?: string;
  alt?: string;
  poster?: string;
  "camera-controls"?: boolean;
  "auto-rotate"?: boolean;
  "rotation-per-second"?: string;
  "shadow-intensity"?: string;
  "shadow-softness"?: string;
  exposure?: string;
  "environment-image"?: string;
  "camera-orbit"?: string;
  "min-camera-orbit"?: string;
  "max-camera-orbit"?: string;
  "field-of-view"?: string;
  "min-field-of-view"?: string;
  "max-field-of-view"?: string;
  "interaction-prompt"?: string;
  loading?: string;
  reveal?: string;
  ar?: boolean;
  "ar-modes"?: string;
  "ar-placement"?: string;
  "ar-scale"?: string;
};

declare module "react" {
  namespace JSX {
    interface IntrinsicElements {
      "model-viewer": ModelViewerAttributes;
    }
  }
}
