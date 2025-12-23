import { Link, Outlet, useLocation } from "react-router-dom";

const navItems = [
  { to: "/app/planning", label: "Planning" },
  { to: "/app/projects/demo-project/missions", label: "Missions" },
  { to: "/app/collaborators", label: "Collaborators" },
  { to: "/app/settings", label: "Settings" },
];

export const AppLayout = () => {
  const location = useLocation();
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b bg-gray-50">
        <div className="mx-auto max-w-5xl px-4 py-3 flex items-center justify-between">
          <div>
            <p className="text-lg font-semibold">Samu</p>
            <p className="text-xs text-gray-600">Phase 2 bootstrap shell</p>
          </div>
          <nav className="flex items-center gap-4 text-sm">
            {navItems.map((item) => {
              const isActive = location.pathname.startsWith(item.to.replace(/:\\w+/, ""));
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={isActive ? "font-semibold text-blue-700" : "text-gray-700"}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl flex-1 px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
};
