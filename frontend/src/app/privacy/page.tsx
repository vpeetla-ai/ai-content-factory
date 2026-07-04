export default function PrivacyPage() {
  return (
    <main className="min-h-screen p-6 max-w-2xl mx-auto text-sm leading-relaxed">
      <h1 className="text-xl font-bold mb-6">Privacy Policy</h1>
      <p className="text-muted mb-4">Last updated: 2026-07-03</p>

      <p className="mb-4">
        This page explains what data AI Content Factory collects, why, and how it is used.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Account data</h2>
      <p className="mb-4">
        We store your email, name, and role as provided by Clerk during sign-in, and the topics
        and drafts generated during your pipeline runs.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Connected platform tokens</h2>
      <p className="mb-4">
        When you connect LinkedIn or X, we store the OAuth access token issued by that platform so
        we can publish approved drafts on your behalf. Tokens are stored server-side and are never
        returned to the browser or exposed via any API response. You can disconnect at any time by
        revoking access from your LinkedIn or X account settings, which invalidates the token on
        the platform's side.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Content sent to AI providers</h2>
      <p className="mb-4">
        Topics and research context are sent to the configured LLM provider to generate drafts.
        We do not sell or share this data with third parties beyond the LLM provider necessary to
        generate your content and the observability provider (Langfuse) used to trace and debug
        agent runs.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Invite codes</h2>
      <p className="mb-4">
        During this invite-only phase, we record which invite code was used to create an account
        and how many times it has been used, with no other identifying information tied to the
        code itself.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Data retention and deletion</h2>
      <p className="mb-4">
        You can request deletion of your account and associated data at any time via the
        project's GitHub issues. Connected platform tokens are deleted immediately on request.
      </p>
    </main>
  );
}
