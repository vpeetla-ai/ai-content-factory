import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/privacy",
  "/terms",
]);
const clerkEnabled = Boolean(
  process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY && process.env.CLERK_SECRET_KEY
);

export default clerkEnabled
  ? clerkMiddleware(async (auth, request) => {
      if (isPublicRoute(request)) {
        return NextResponse.next();
      }
      const { userId } = await auth();
      if (!userId) {
        const signIn = new URL("/sign-in", request.url);
        signIn.searchParams.set("redirect_url", request.url);
        return NextResponse.redirect(signIn);
      }
      return NextResponse.next();
    })
  : () => NextResponse.next();

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
