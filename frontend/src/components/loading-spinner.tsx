"use client";
import { Spinner } from "@/components/ui/shadcn-io/spinner";

const LoadingSpinner = () => {
  return (
    <div className="grid h-screen w-full grid-cols-4 items-center justify-center gap-8">
      <Spinner key={"ring"} variant={"ring"} />
      <span className="ml-3 text-gray-600">Carregando...</span>
    </div>
  );
};

export default LoadingSpinner;
