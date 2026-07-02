/** @type {import('next').NextConfig} */
const productionApi = "https://acf-api-eub4.onrender.com";
const isVercel = process.env.VERCEL === "1";

const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL:
      process.env.NEXT_PUBLIC_API_URL ||
      (isVercel ? `${productionApi}/api/v1` : "http://localhost:8000/api/v1"),
    NEXT_PUBLIC_WS_URL:
      process.env.NEXT_PUBLIC_WS_URL || (isVercel ? productionApi : "http://localhost:8000"),
  },
};

module.exports = nextConfig;
