import { useParams } from "react-router-dom";

export const MissionListPage = () => {
  const { projectId } = useParams();

  return (
    <section>
      <h1>Missions</h1>
      <p>Project: {projectId ?? "unknown project"}</p>
    </section>
  );
};
