import { WorkspaceShell } from "@/components/workspace-shell";

export default function HomePage() {
  return (
    <WorkspaceShell
      title="Local MVP shell"
      description="This app shell establishes the route structure and shared layout for the provider workspace."
    >
      <section className="rounded-xl border border-slate-200 bg-slate-50 p-6">
        <h2 className="text-xl font-semibold text-slate-900">Front-end foundation</h2>
        <p className="mt-3 text-slate-700">
          The workspace shell provides the starting layout for provider-facing pages and keeps route state easy to extend.
        </p>
      </section>
    </WorkspaceShell>
  );
}
