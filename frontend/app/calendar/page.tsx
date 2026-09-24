import { WorkspaceShell } from "@/components/workspace-shell";

export default function CalendarPage() {
  return (
    <WorkspaceShell
      title="Calendar"
      description="Placeholder calendar route for the provider workspace."
    >
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-6">
        <p className="text-slate-700">This route will later represent scheduling or availability panels.</p>
      </div>
    </WorkspaceShell>
  );
}
