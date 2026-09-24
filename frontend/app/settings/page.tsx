import { WorkspaceShell } from "@/components/workspace-shell";

export default function SettingsPage() {
  return (
    <WorkspaceShell
      title="Settings"
      description="Placeholder settings route for the provider workspace."
    >
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-6">
        <p className="text-slate-700">This route will later expose configuration and workspace preferences.</p>
      </div>
    </WorkspaceShell>
  );
}
