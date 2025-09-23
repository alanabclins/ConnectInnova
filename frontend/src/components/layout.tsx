import React from "react";
import { Outlet } from "react-router-dom";

const Layout: React.FC = () => {
  return (
    <div className="">
        <main >
          <Outlet />
        </main>
    </div>
  );
};

export default Layout;
