"use client";

import { ClerkProvider } from "@clerk/nextjs";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

// Client bundle only has NEXT_PUBLIC_* vars — never check CLERK_SECRET_KEY here
const clerkEnabled = Boolean(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY);

export function Providers({ children }: { children: React.ReactNode }) {
  const [client] = useState(() => new QueryClient());

  const tree = <QueryClientProvider client={client}>{children}</QueryClientProvider>;

  if (!clerkEnabled) {
    return tree;
  }

  return (
    <ClerkProvider
      publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!}
      signInUrl="/sign-in"
      signUpUrl="/sign-up"
      signInFallbackRedirectUrl="/"
      signUpFallbackRedirectUrl="/"
    >
      {tree}
    </ClerkProvider>
  );
}

export const isClerkEnabled = clerkEnabled;
