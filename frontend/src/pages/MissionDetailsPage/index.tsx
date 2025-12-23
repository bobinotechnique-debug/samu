import { useParams } from "react-router-dom";

export const MissionDetailsPage = () => {
  const { projectId, missionId } = useParams();

  return (
    <section>
      <h1>Mission Details</h1>
      <p>Project: {projectId ?? "unknown project"}</p>
      <p>Mission: {missionId ?? "unknown mission"}</p>
    </section>
  );
};
