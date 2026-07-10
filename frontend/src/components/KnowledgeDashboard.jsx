import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
  createTask,
  fetchAnalytics,
  fetchDocuments,
  fetchTasks,
  fetchUsers,
  searchDocuments,
  updateTask,
  uploadDocument,
} from "../api/knowledge";

export default function KnowledgeDashboard() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [users, setUsers] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [taskTitle, setTaskTitle] = useState("");
  const [taskDescription, setTaskDescription] = useState("");
  const [assignedToId, setAssignedToId] = useState("");
  const [uploadTitle, setUploadTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");
  const [loading, setLoading] = useState(true);

  const isAdmin = useMemo(() => user?.role_name === "admin", [user]);

  async function loadData() {
    setLoading(true);
    try {
      const [tasksData, documentsData, analyticsData] = await Promise.all([
        fetchTasks(),
        fetchDocuments(),
        fetchAnalytics(),
      ]);
      setTasks(tasksData);
      setDocuments(documentsData);
      setAnalytics(analyticsData);
      if (isAdmin) {
        const usersData = await fetchUsers();
        setUsers(usersData);
        if (usersData[0]) setAssignedToId(usersData[0].id);
      }
    } catch (error) {
      setStatusMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [isAdmin]);

  async function handleCreateTask(event) {
    event.preventDefault();
    if (!taskTitle.trim()) return;
    try {
      const newTask = await createTask(taskTitle, taskDescription, Number(assignedToId || 0));
      setTasks((prev) => [newTask, ...prev]);
      setTaskTitle("");
      setTaskDescription("");
      setStatusMessage("Task created successfully.");
    } catch (error) {
      setStatusMessage(error.message);
    }
  }

  async function handleCompleteTask(taskId) {
    try {
      const updatedTask = await updateTask(taskId, "completed");
      setTasks((prev) => prev.map((task) => (task.id === updatedTask.id ? updatedTask : task)));
      setStatusMessage("Task marked complete.");
    } catch (error) {
      setStatusMessage(error.message);
    }
  }

  async function handleUpload(event) {
    event.preventDefault();
    if (!selectedFile) return;
    try {
      const createdDocument = await uploadDocument(uploadTitle || selectedFile.name, selectedFile);
      setDocuments((prev) => [createdDocument, ...prev]);
      setUploadTitle("");
      setSelectedFile(null);
      setStatusMessage("Document uploaded and indexed.");
    } catch (error) {
      setStatusMessage(error.message);
    }
  }

  async function handleSearch(event) {
    event.preventDefault();
    if (!searchQuery.trim()) return;
    try {
      const results = await searchDocuments(searchQuery);
      setSearchResults(results);
      setStatusMessage("Search completed.");
    } catch (error) {
      setStatusMessage(error.message);
    }
  }

  if (loading) {
    return <p className="status-text">Loading knowledge workspace...</p>;
  }

  return (
    <div className="knowledge-dashboard">
      <div className="hero-card">
        <div>
          <p className="eyebrow">AI-powered knowledge workflow</p>
          <h2>Manage documents, search knowledge, and complete assigned work</h2>
          <p>Admins publish documents and tasks. Users search the knowledge base and complete their assigned tasks.</p>
        </div>
        <div className="hero-badge">Signed in as {user?.email}</div>
      </div>

      {statusMessage ? <div className="status-banner">{statusMessage}</div> : null}

      {analytics ? (
        <div className="analytics-grid">
          <div className="stat-card">
            <strong>{analytics.total_tasks}</strong>
            <span>Total tasks</span>
          </div>
          <div className="stat-card">
            <strong>{analytics.completed_tasks}</strong>
            <span>Completed</span>
          </div>
          <div className="stat-card">
            <strong>{analytics.pending_tasks}</strong>
            <span>Pending</span>
          </div>
          <div className="stat-card">
            <strong>{analytics.most_searched_query || "—"}</strong>
            <span>Top search</span>
          </div>
        </div>
      ) : null}

      <div className="panel-grid">
        <section className="panel">
          <h3>Search knowledge base</h3>
          <form onSubmit={handleSearch} className="stacked-form">
            <input
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              placeholder="Ask about policies, onboarding, or procedures"
            />
            <button type="submit">Search</button>
          </form>
          <div className="result-list">
            {searchResults.length === 0 ? <p className="status-text">No results yet.</p> : null}
            {searchResults.map((document) => (
              <article key={document.id} className="card-item">
                <h4>{document.title}</h4>
                <p>{document.content_text.slice(0, 220)}{document.content_text.length > 220 ? "..." : ""}</p>
              </article>
            ))}
          </div>
        </section>

        {isAdmin ? (
          <section className="panel">
            <h3>Upload document</h3>
            <form onSubmit={handleUpload} className="stacked-form">
              <input
                value={uploadTitle}
                onChange={(event) => setUploadTitle(event.target.value)}
                placeholder="Document title"
              />
              <input type="file" onChange={(event) => setSelectedFile(event.target.files?.[0] || null)} />
              <button type="submit">Upload</button>
            </form>
            <h3>Create task</h3>
            <form onSubmit={handleCreateTask} className="stacked-form">
              <input value={taskTitle} onChange={(event) => setTaskTitle(event.target.value)} placeholder="Task title" />
              <input value={taskDescription} onChange={(event) => setTaskDescription(event.target.value)} placeholder="Task description" />
              <select value={assignedToId} onChange={(event) => setAssignedToId(event.target.value)}>
                {users.map((userOption) => (
                  <option key={userOption.id} value={userOption.id}>
                    {userOption.email}
                  </option>
                ))}
              </select>
              <button type="submit">Assign task</button>
            </form>
          </section>
        ) : null}
      </div>

      <section className="panel">
        <h3>Tasks</h3>
        <div className="task-list">
          {tasks.map((task) => (
            <article key={task.id} className="card-item task-item">
              <div>
                <h4>{task.title}</h4>
                <p>{task.description}</p>
                <small>Status: {task.status}</small>
              </div>
              {task.status !== "completed" ? (
                <button onClick={() => handleCompleteTask(task.id)}>Mark complete</button>
              ) : (
                <span className="pill">Completed</span>
              )}
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <h3>Knowledge documents</h3>
        <div className="document-list">
          {documents.map((document) => (
            <article key={document.id} className="card-item">
              <h4>{document.title}</h4>
              <p>{document.filename}</p>
              <small>{document.content_type}</small>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
