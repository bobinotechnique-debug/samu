import { Link, Outlet } from "react-router-dom";

const demoProjectId = "project-demo";
const demoMissionId = "mission-demo";

export const AppLayout = () => {
  return (
    <div className="app-layout">
      <header>
        <h1>Samu Console</h1>
        <nav>
          <ul>
            <li>
              <Link to="/app/planning">Planning</Link>
            </li>
            <li>
              <Link to={`/app/projects/${demoProjectId}/missions`}>Missions</Link>
            </li>
            <li>
              <Link to={`/app/projects/${demoProjectId}/missions/${demoMissionId}`}>Mission details</Link>
            </li>
            <li>
              <Link to="/app/collaborators">Collaborators</Link>
            </li>
            <li>
              <Link to="/app/settings">Settings</Link>
            </li>
          </ul>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
};
