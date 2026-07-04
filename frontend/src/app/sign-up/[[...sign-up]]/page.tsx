"use client";

import { useState } from "react";
import { SignUp } from "@clerk/nextjs";
import { setInviteCode, getInviteCode } from "@/lib/invite";

export default function SignUpPage() {
  const [code, setCode] = useState("");
  const [unlocked, setUnlocked] = useState(!!getInviteCode());

  if (!unlocked) {
    return (
      <main className="min-h-screen flex items-center justify-center p-6">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            setInviteCode(code.trim());
            setUnlocked(true);
          }}
          className="bg-panel border border-white/10 rounded-xl p-6 w-full max-w-sm space-y-4"
        >
          <h1 className="text-lg font-bold">AI Content Factory is invite-only</h1>
          <p className="text-sm text-muted">Enter your invite code to create an account.</p>
          <input
            autoFocus
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Invite code"
            className="w-full bg-surface border border-white/10 rounded-lg p-3 text-sm focus:outline-none focus:border-accent"
          />
          <button
            type="submit"
            disabled={!code.trim()}
            className="w-full px-4 py-2 rounded-lg bg-accent hover:bg-accent/80 disabled:opacity-50 text-white font-semibold text-sm transition"
          >
            Continue
          </button>
          <p className="text-xs text-muted">
            The code is checked when your account is created — an invalid code will be rejected
            at that step.
          </p>
          <p className="text-xs text-muted">
            By continuing you agree to the{" "}
            <a href="/terms" className="underline">
              Terms
            </a>{" "}
            and{" "}
            <a href="/privacy" className="underline">
              Privacy Policy
            </a>
            .
          </p>
        </form>
      </main>
    );
  }

  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <SignUp routing="path" path="/sign-up" signInUrl="/sign-in" />
    </main>
  );
}
