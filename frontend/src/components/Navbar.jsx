import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav className="navbar">
      <span className="navbar-title">Todo App</span>
      {user && (
        <div className="navbar-right">
          <span>{user.email}</span>
          <button onClick={handleLogout}>Log out</button>
        </div>
      )}
    </nav>
  );
}
