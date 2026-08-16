import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [news, setNews] = useState([]);
  const [search, setSearch] = useState("");
  const [source, setSource] = useState("All");
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = () => {
    setLoading(true);
    setError("");

    axios
      .get(
        "https://syntecxhubnews-intelligence-dashboard-production.up.railway.app/api/news"
      )
      .then((response) => {
        setNews(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setError("Unable to load news. Please try again.");
        setLoading(false);
      });
  };

  const sources = [
    "All",
    ...new Set(news.map((article) => article.source).filter(Boolean)),
  ];

  const categories = [
    "All",
    ...new Set(news.map((article) => article.category).filter(Boolean)),
  ];

  const filteredNews = news.filter((article) => {
    const matchesSearch = article.title
      ?.toLowerCase()
      .includes(search.toLowerCase());

    const matchesSource =
      source === "All" || article.source === source;

    const matchesCategory =
      category === "All" || article.category === category;

    return matchesSearch && matchesSource && matchesCategory;
  });

  const sourceCount = (name) =>
    news.filter((article) => article.source === name).length;

  const categoryCount = (name) =>
    news.filter((article) => article.category === name).length;

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div>
          <div className="brand">
            <span className="brand-icon">📰</span>
            <span>News Intelligence</span>
          </div>

          <p className="subtitle">
            Automated news monitoring and AI-powered classification
          </p>
        </div>

        <button className="refresh-btn" onClick={fetchNews}>
          ↻ Refresh
        </button>
      </header>

      {/* Statistics */}
      <section className="stats">

        <div className="stat-card">
          <div className="stat-icon">📰</div>
          <div>
            <p>Total Articles</p>
            <h2>{news.length}</h2>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🌐</div>
          <div>
            <p>News Sources</p>
            <h2>{sources.length - 1}</h2>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🤖</div>
          <div>
            <p>AI Categories</p>
            <h2>{categories.length - 1}</h2>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⏰</div>
          <div>
            <p>Auto Scraping</p>
            <h2>30 min</h2>
          </div>
        </div>

      </section>

      {/* Category Overview */}
      <section className="source-section">
        <h2>AI Category Overview</h2>

        <div className="source-list">
          {categories
            .filter((item) => item !== "All")
            .map((item) => (
              <div className="source-item" key={item}>
                <span>{item}</span>
                <strong>{categoryCount(item)}</strong>
              </div>
            ))}
        </div>
      </section>

      {/* Search and Filters */}
      <section className="controls">

        <div className="search-box">
          <span>🔍</span>

          <input
            type="text"
            placeholder="Search news headlines..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
        >
          {sources.map((item) => (
            <option key={item} value={item}>
              {item === "All" ? "All Sources" : item}
            </option>
          ))}
        </select>

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {categories.map((item) => (
            <option key={item} value={item}>
              {item === "All" ? "All Categories" : item}
            </option>
          ))}
        </select>

      </section>

      {/* News */}
      <section className="news-section">

        <div className="section-heading">
          <div>
            <h2>Latest News</h2>
            <p>{filteredNews.length} articles found</p>
          </div>
        </div>

        {loading && (
          <div className="message">
            Loading latest news...
          </div>
        )}

        {error && (
          <div className="message error">
            {error}
          </div>
        )}

        {!loading && !error && filteredNews.length === 0 && (
          <div className="message">
            No articles found.
          </div>
        )}

        <div className="news-grid">

          {!loading &&
            !error &&
            filteredNews.map((article) => (
              <article className="news-card" key={article.id}>

                <div className="card-top">

                  <span className="source-badge">
                    {article.source}
                  </span>

                  <span className="category-badge">
                    🤖 {article.category || "Uncategorized"}
                  </span>

                </div>

                <h3>{article.title}</h3>

                <p className="published">
                  🕒 {article.published || "Date unavailable"}
                </p>

                <div className="card-bottom">

                  <span className="scraped">
                    AI classified
                  </span>

                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Read Article →
                  </a>

                </div>

              </article>
            ))}

        </div>

      </section>

      <footer>
        <p>
          News Intelligence Dashboard • Automated News Collection + AI Classification
        </p>
      </footer>

    </div>
  );
}

export default App;
