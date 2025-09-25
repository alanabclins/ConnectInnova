import React from "react";
import { Outlet } from "react-router-dom";

const Layout: React.FC = () => {
  return (
    <div className="">
      <script src="https://unpkg.com/feather-icons"></script>
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
