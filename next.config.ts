import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  /* tipovne napake se NE prikrivajo več — tsc je čist od P17
     (prej: ignoreBuildErrors: true je prikrival 34 napak) */
  reactStrictMode: false,
};

export default nextConfig;
