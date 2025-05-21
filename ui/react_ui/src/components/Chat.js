import React from 'react';
import { FileText, Search, Send } from 'lucide-react';

function Chat({ 
  query, 
  setQuery, 
  response, 
  sources, 
  mode, 
  modeDisplayName, 
  isLoading, 
  handleSubmit 
}) {
  // Sample documents data for the sidebar
  const documents = [
    { 
      title: "Declaration of Independence", 
      date: "July 4, 1776", 
      authors: ["Thomas Jefferson", "Continental Congress"],
      type: "founding_document"
    },
    { 
      title: "Common Sense", 
      date: "January 10, 1776", 
      authors: ["Thomas Paine"],
      type: "pamphlet"
    },
    { 
      title: "Letter from Abigail Adams to John Adams", 
      date: "March 31, 1776", 
      authors: ["Abigail Adams"],
      type: "letter"
    },
  ];

  return (
    <div className="flex-1 flex">
      <div className="flex-1 flex flex-col p-4 overflow-auto">
        <div className="flex-1 overflow-auto mb-4">
          {response && (
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-4">
              <h3 className="font-semibold text-gray-700 mb-2">
                {modeDisplayName}
              </h3>
              <p className="text-gray-800 whitespace-pre-wrap">{response}</p>
              
              {sources && sources.length > 0 && (
                <div className="mt-4 pt-3 border-t border-gray-200">
                  <h4 className="text-sm font-semibold text-gray-600 mb-1">Sources:</h4>
                  <ul className="text-sm text-gray-600">
                    {sources.map((source, index) => (
                      <li key={index} className="flex items-center">
                        <FileText className="w-3 h-3 mr-1 text-gray-400" />
                        {source}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
        
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Ask about American Independence..."
              className="w-full py-3 px-4 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <Search className="absolute right-3 top-3.5 h-4 w-4 text-gray-400" />
          </div>
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg flex items-center"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : (
              <span className="flex items-center">
                <Send className="w-4 h-4 mr-2" />
                Ask
              </span>
            )}
          </button>
        </form>
      </div>

      {/* Right sidebar for sources */}
      {response && (
        <div className="w-64 bg-white border-l border-gray-200 p-4 overflow-auto">
          <h2 className="font-semibold text-gray-600 mb-3">Source Documents</h2>
          {sources && sources.map((source, idx) => {
            const doc = documents.find(d => d.title.includes(source));
            return doc ? (
              <div key={idx} className="mb-4 pb-4 border-b border-gray-100 last:border-b-0">
                <h3 className="font-medium text-sm text-gray-800">{doc.title}</h3>
                <div className="text-xs text-gray-600 mt-1">{doc.date}</div>
                <div className="text-xs text-gray-600">{doc.authors.join(", ")}</div>
                <div className="mt-2">
                  <span className="inline-block px-1.5 py-0.5 text-xs bg-blue-100 text-blue-800 rounded">
                    {doc.type}
                  </span>
                </div>
              </div>
            ) : null;
          })}

          <div className="mt-6">
            <h2 className="font-semibold text-gray-600 mb-2">Evaluation</h2>
            <div className="space-y-2">
              <div>
                <div className="text-xs font-medium text-gray-600">Response Relevance</div>
                <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                  <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '85%' }}></div>
                </div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-600">Historical Accuracy</div>
                <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                  <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '90%' }}></div>
                </div>
              </div>
              <div>
                <div className="text-xs font-medium text-gray-600">Source Quality</div>
                <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                  <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '95%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chat;
