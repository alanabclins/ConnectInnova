import { Navigate } from "react-router-dom";
import { useAuth } from "../auth/authContext";
import LoadingSpinner from "../components/loading-spinner";

const RootRedirect = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  console.log(user);

  return user ? (
    <Navigate to="/home" replace />
  ) : (
    <Navigate to="/login" replace />
  );
};

export default RootRedirect;
