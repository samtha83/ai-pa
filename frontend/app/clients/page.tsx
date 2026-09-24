import { WorkspaceShell } from "@/components/workspace-shell";

export default function ClientsPage() {
  return (
    <WorkspaceShell
      title="Clients"
      description="Placeholder clients route for the provider workspace."
    >
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-6">
        <p className="text-slate-700">This route will later show provider-facing client records and actions.</p>
      </div>
    </WorkspaceShell>
  );
}
