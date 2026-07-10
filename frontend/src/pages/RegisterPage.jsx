import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function RegisterPage() {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();


  async function handleSubmit(e) {
    e.preventDefault();

    setError("");
    setSubmitting(true);

    try {

      await register(email, password);

      navigate("/login", {
        state: { email, message: "Account created successfully. Please log in." }
      });


    } catch (err) {

      setError(err.message || "Registration failed");

    } finally {

      setSubmitting(false);

    }
  }


  return (
    <div className="auth-page">

      <form 
        onSubmit={handleSubmit} 
        className="auth-form"
      >

        <h2>Create Account</h2>


        {error && (
          <p className="error-text">
            {error}
          </p>
        )}


        <input
          type="email"
          placeholder="Enter Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
          required
        />


        <input
          type="password"
          placeholder="Password (minimum 8 characters)"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
          minLength={8}
          required
        />


        <button 
          type="submit"
          disabled={submitting}
        >
          {submitting ? "Creating account..." : "Register"}
        </button>


        <p>
          Already have an account?{" "}
          <Link to="/login">
            Login
          </Link>
        </p>


      </form>

    </div>
  );
}