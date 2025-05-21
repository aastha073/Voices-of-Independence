import React, { useState } from 'react';
import { BookOpen, Calendar, Clock, FileText, Search, Send, User } from 'lucide-react';
import './styles/App.css';
import Chat from './components/Chat';
import Documents from './components/Documents';
import Timeline from './components/Timeline';

function App() {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('historian');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState('');
  const [sources, setSources] = useState([]);
  const [selectedTab, setSelectedTab] = useState('chat');

  // Mock API call - in real app, this would call your backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsLoading(true);
    
    // Simulate API call
    try {
      const response = await fetch('/api/independence-rag', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          mode,
          limit: 5
        }),
      });
      
      const data = await response.json();
      setResponse(data.response);
      setSources(data.sources);
    } catch (error) {
      console.error('Error:', error);
      setResponse("Error connecting to the server. Please try again later.");
      setSources([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleModeChange = (newMode) => {
    setMode(newMode);
  };

  // Maps for display values
  const modeDisplayNames = {
    'historian': 'Expert Historian',
    'founding_father': 'Benjamin Franklin',
    'time_traveler': 'Time-Traveling Guide'
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-900 text-white p-4">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold flex items-center">
            <span className="mr-2">🎆</span> Voices of Independence
          </h1>
          <p className="text-blue-200">An AI-Powered Time Travel Through 1776</p>
        </div>
      </header>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left sidebar */}
        <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
          <div className="p-4">
            <h2 className="font-semibold text-gray-600 mb-2">Response Mode</h2>
            <div className="space-y-1">
              <button
                className={`w-full text-left px-3 py-2 rounded-md ${mode === 'historian' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`}
                onClick={() => handleModeChange('historian')}
              >
                <div className="flex items-center">
                  <BookOpen className="w-4 h-4 mr-2" />
                  <span>Expert Historian</span>
                </div>
              </button>
              <button
                className={`w-full text-left px-3 py-2 rounded-md ${mode === 'founding_father' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`}
                onClick={() => handleModeChange('founding_father')}
              >
                <div className="flex items-center">
                  <User className="w-4 h-4 mr-2" />
                  <span>Benjamin Franklin</span>
                </div>
              </button>
              <button
                className={`w-full text-left px-3 py-2 rounded-md ${mode === 'time_traveler' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`}
                onClick={() => handleModeChange('time_traveler')}
              >
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-2" />
                  <span>Time Traveler</span>
                </div>
              </button>
            </div>
          </div>
          
          <div className="p-4 border-t border-gray-200">
            <h2 className="font-semibold text-gray-600 mb-2">Example Questions</h2>
            <ul className="text-sm space-y-1 text-gray-600">
              <li className="cursor-pointer hover:text-blue-600" onClick={() => setQuery("What were the key arguments for independence in 1776?")}>
                • Key arguments for independence?
              </li>
              <li className="cursor-pointer hover:text-blue-600" onClick={() => setQuery("What did the founders believe about taxation?")}>
                • Founders' views on taxation?
              </li>
              <li className="cursor-pointer hover:text-blue-600" onClick={() => setQuery("What grievances did colonists have against King George?")}>
                • Grievances against King George?
              </li>
            </ul>
          </div>
          
          <div className="mt-auto p-4 border-t border-gray-200">
            <h2 className="font-semibold text-gray-600 mb-2">About</h2>
            <p className="text-xs text-gray-500">
              Powered by Weaviate, FriendliAI, and Comet Opik. All responses are generated based on historical documents from the American Revolutionary period.
            </p>
          </div>
        </div>

        {/* Main content area */}
        <div className="flex-1 flex flex-col">
          <div className="flex border-b border-gray-200">
            <button
              className={`px-4 py-2 font-medium ${selectedTab === 'chat' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-800'}`}
              onClick={() => setSelectedTab('chat')}
            >
              Chat
            </button>
            <button
              className={`px-4 py-2 font-medium ${selectedTab === 'documents' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-800'}`}
              onClick={() => setSelectedTab('documents')}
            >
              Documents
            </button>
            <button
              className={`px-4 py-2 font-medium ${selectedTab === 'timeline' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600 hover:text-gray-800'}`}
              onClick={() => setSelectedTab('timeline')}
            >
              Timeline
            </button>
          </div>

          {selectedTab === 'chat' && (
            <Chat 
              query={query}
              setQuery={setQuery}
              response={response}
              sources={sources}
              mode={mode}
              modeDisplayName={modeDisplayNames[mode]}
              isLoading={isLoading}
              handleSubmit={handleSubmit}
            />
          )}

          {selectedTab === 'documents' && <Documents />}
          
          {selectedTab === 'timeline' && <Timeline />}
        </div>
      </div>
    </div>
  );
}

export default App;
