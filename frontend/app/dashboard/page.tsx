import { WorkspaceShell } from "@/components/workspace-shell";

export default function DashboardPage() {
  return (
    <WorkspaceShell
      title="Dashboard"
      description="Placeholder dashboard route for the provider workspace."
    >
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-6">
        <p className="text-slate-700">This page will house provider metrics and overview panels in later features.</p>
      </div>
    </WorkspaceShell>
  );
}
