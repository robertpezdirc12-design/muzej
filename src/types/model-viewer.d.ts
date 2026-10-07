import type { DOMAttributes } from "react";

/** JSX tipi za <model-viewer> (Google, @google/model-viewer) — React 19 podpira custom elemente. */
export type ModelViewerAttributes = DOMAttributes<HTMLElement> & {
  src?: string;
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
  "min-field-of-view"?: string;
  "max-field-of-view"?: string;
  "max-camera-orbit"?: string;
  "interaction-prompt"?: string;
  loading?: string;
  reveal?: string;
  ar?: boolean;
};

declare module "react" {
  namespace JSX {
    interface IntrinsicElements {
      "model-viewer": ModelViewerAttributes;
    }
  }
}
