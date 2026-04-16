import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import SearchPage from './pages/SearchPage'
import FailurePage from './pages/FailurePage'
import AnalyzePage from './pages/AnalyzePage'

function App() {
  return (
    <div className="min-h-screen text-text-primary font-mono bg-transparent">
      <Navbar />
      <main className="pt-20 px-6 max-w-7xl mx-auto pb-24">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/failure/:id" element={<FailurePage />} />
          <Route path="/analyze" element={<AnalyzePage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
