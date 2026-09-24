"use client";

export default function Error({ reset }: { reset: () => void }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-6">
      <div className="max-w-md rounded-xl border border-red-200 bg-white p-8 text-center shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">Something went wrong</h1>
        <p className="mt-4 text-slate-700">The application failed to render this route.</p>
        <button
          type="button"
          onClick={() => reset()}
          className="mt-6 rounded-md bg-red-600 px-4 py-2 font-medium text-white transition hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          Try again
        </button>
      </div>
    </main>
  );
}
