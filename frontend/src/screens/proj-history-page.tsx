import { ProjectStepper } from "@/components/project-stories-stepper";
import { defineStepper } from "@/components/ui/stepper";
import { useLocation, useNavigate } from "react-router-dom";
import type { ProjectDetails } from "@/types/project.types";

const { Stepper } = defineStepper(
  { id: "step-1", title: "Step 1" },
  { id: "step-2", title: "Step 2" },
  { id: "step-3", title: "Step 3" }
);

interface ProjUserStoriesProps {
  projectToEdit?: ProjectDetails;
  isEditing?: boolean;
  onClose?: () => void;
}

export default function ProjUserStories(props: ProjUserStoriesProps) {
  const navigate = useNavigate();
  const location = useLocation();

  const { projectToEdit: locationProject, isEditing: locationEditing } = (
    location.state || {}
  ) as {
    projectToEdit?: ProjectDetails;
    isEditing?: boolean;
  };

  const isEditing = props.isEditing ?? locationEditing ?? false;
  const projectToEdit = props.projectToEdit ?? locationProject;

  const handleComplete = (result: {
    projectId: string;
    projectData: { project_title: string; project_description: string };
  }) => {
    if (props.onClose) {
      props.onClose();
    } else {
      navigate("/home/summary", {
        state: {
          projectId: result.projectId,
          projectData: result.projectData,
        },
      });
    }
  };

  return (
    <Stepper.Provider>
      <div className="py-6 px-8">
        <ProjectStepper
          isEditing={isEditing}
          projectToEdit={projectToEdit}
          onComplete={handleComplete}
        />
      </div>
    </Stepper.Provider>
  );
}