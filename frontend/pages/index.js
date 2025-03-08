import { useEffect, useState } from "react";

const Home = () => {
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async (retryCount = 3) => {
      try {
        setError(null);
        const res = await fetch("http://localhost:5000/api/opportunities", {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        
        if (!res.ok) {
          throw new Error(`Server responded with status: ${res.status}`);
        }
        
        const data = await res.json();
        setOpportunities(data);
      } catch (err) {
        if (retryCount > 0) {
          console.warn(`Retrying... (${3 - retryCount + 1})`);
          fetchData(retryCount - 1);
        } else {
          console.error("Failed to fetch opportunities:", err);
          setError(`Connection failed: ${err.message}. Please ensure the backend server is running on port 5000.`);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <div style={{ padding: "20px", fontFamily: "Arial", color: "red" }}>
        <h1>Error</h1>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Money-Making Opportunities</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#f2f2f2" }}>
              <th style={{ padding: "10px" }}>Product Name</th>
              <th style={{ padding: "10px" }}>Price</th>
              <th style={{ padding: "10px" }}>Last Updated</th>
            </tr>
          </thead>
          <tbody>
            {opportunities.map((item, index) => (
              <tr key={index} style={{ borderBottom: "1px solid #ddd" }}>
                <td style={{ padding: "10px" }}>{item.name}</td>
                <td style={{ padding: "10px" }}>{item.price}</td>
                <td style={{ padding: "10px" }}>{item.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Home;