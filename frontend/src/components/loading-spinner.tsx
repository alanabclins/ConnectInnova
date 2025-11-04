"use client";
import { Spinner } from "@/components/ui/shadcn-io/spinner";

const LoadingSpinner = () => {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-4">
      <Spinner variant={"circle"} size={32} className="text-primary" />
      <h1 className="ml-3 text-gray-600 font-medium text-lg">Carregando...</h1>
    </div>
  );
};

export default LoadingSpinner;
