import { ProjectStepper } from "@/components/project-stories-stepper";
import { defineStepper } from "@/components/ui/stepper";

const { Stepper } = defineStepper(
  { id: "step-1", title: "Step 1" },
  { id: "step-2", title: "Step 2" },
  { id: "step-3", title: "Step 3" }
);

export default function ProjUserStories() {
  return (
    <Stepper.Provider>
      <ProjectStepper />
    </Stepper.Provider>
  );
}
