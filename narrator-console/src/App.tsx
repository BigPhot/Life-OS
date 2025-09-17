import React from 'react';

const App: React.FC = () => {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Narrator Console</h1>
        <p>Welcome to your life tracking and visualization desktop application!</p>
      </header>

      <main className="app-main">
        <div className="welcome-section">
          <h2>Hello World</h2>
          <p>
            This is the initial setup of your Narrator Console application.
            Built with Electron, React, and TypeScript.
          </p>

          <div className="features-preview">
            <h3>Upcoming Features:</h3>
            <ul>
              <li>📅 Current Day Console</li>
              <li>📖 Era Visualization</li>
              <li>🌐 3D Task Graph</li>
              <li>🧠 Knowledge Graph</li>
            </ul>
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>Powered by Electron + React + TypeScript + Vite</p>
      </footer>
    </div>
  );
};

export default App;