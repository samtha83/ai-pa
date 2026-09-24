import { WorkspaceShell } from "@/components/workspace-shell";

export default function LoginPage() {
  return (
    <WorkspaceShell
      title="Login"
      description="Placeholder login screen for the provider workspace."
    >
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-6">
        <p className="text-slate-700">Authentication is intentionally out of scope for this MVP shell.</p>
      </div>
    </WorkspaceShell>
  );
}
