export default function TermsPage() {
  return (
    <main className="min-h-screen p-6 max-w-2xl mx-auto text-sm leading-relaxed">
      <h1 className="text-xl font-bold mb-6">Terms of Service</h1>
      <p className="text-muted mb-4">Last updated: 2026-07-03</p>

      <p className="mb-4">
        AI Content Factory is an invite-only, early-access tool that turns a topic into
        platform-ready drafts using AI agents, with a human-in-the-loop review step before
        anything is published. By using it, you agree to the following.
      </p>

      <h2 className="font-semibold mt-6 mb-2">What the service does</h2>
      <p className="mb-4">
        You provide a topic. The service generates draft content for LinkedIn, X, Substack,
        Medium, and Instagram. You review and approve or edit each draft before publish. For
        LinkedIn and X, an approved draft is posted to your connected account via the official
        platform API using your own OAuth-granted access. For Substack, Medium, and Instagram,
        the service returns a copy-ready draft instead of auto-publishing, since no viable public
        posting API exists for those platforms today.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Your responsibility for published content</h2>
      <p className="mb-4">
        You are solely responsible for reviewing and approving any content before it is
        published under your account. This service does not replace legal, brand, or compliance
        review for regulated industries or claims that require substantiation.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Connected accounts</h2>
      <p className="mb-4">
        Connecting LinkedIn or X grants the service permission to post on your behalf, limited to
        the scopes requested at connect time. You can revoke this access at any time from your
        LinkedIn or X account settings.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Invite-only access, no warranty</h2>
      <p className="mb-4">
        This is an early-access product provided as-is, without warranty of any kind, while it is
        invite-gated and free of charge. Features, availability, and these terms may change as the
        service matures.
      </p>

      <h2 className="font-semibold mt-6 mb-2">Contact</h2>
      <p>Questions about these terms can be raised via the project's GitHub issues.</p>
    </main>
  );
}
