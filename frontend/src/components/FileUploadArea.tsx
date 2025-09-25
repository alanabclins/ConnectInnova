import React, { useCallback } from "react";
import { IconUpload } from "@tabler/icons-react";
import { Input } from "./ui/input";

interface FileUploadAreaProps {
  onFilesSelected?: (files: FileList) => void;
}

export const FileUploadArea: React.FC<FileUploadAreaProps> = ({
  onFilesSelected,
}) => {
  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      const files = e.dataTransfer.files;
      if (files.length > 0 && onFilesSelected) {
        onFilesSelected(files);
      }
    },
    [onFilesSelected]
  );

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  }, []);

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && onFilesSelected) {
        onFilesSelected(files);
      }
    },
    [onFilesSelected]
  );

  return (
    <div
      className="relative border-2 border-dashed border-upload-border rounded-lg py-18 md:py-32 bg-upload-bg hover:border-primary/50 transition-colors cursor-pointer"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onClick={() => document.getElementById("file-upload")?.click()}
    >
      <Input
        id="file-upload"
        type="file"
        multiple
        className="hidden"
        onChange={handleFileInput}
      />
      <div className="flex flex-col items-center justify-center text-center">
        <IconUpload className="w-8 h-8 text-muted-foreground mb-4" />
        <p className="text-foreground font-medium">Fazer upload de arquivos</p>
      </div>
    </div>
  );
};
