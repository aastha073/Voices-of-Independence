import React from 'react';
import { Calendar } from 'lucide-react';

function Documents() {
  // Sample documents data
  const documents = [
    { 
      title: "Declaration of Independence", 
      date: "July 4, 1776", 
      authors: ["Thomas Jefferson", "Continental Congress"],
      type: "founding_document",
      excerpt: "We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness."
    },
    { 
      title: "Common Sense", 
      date: "January 10, 1776", 
      authors: ["Thomas Paine"],
      type: "pamphlet",
      excerpt: "Society in every state is a blessing, but government even in its best state is but a necessary evil; in its worst state an intolerable one."
    },
    { 
      title: "Letter from Abigail Adams to John Adams", 
      date: "March 31, 1776", 
      authors: ["Abigail Adams"],
      type: "letter",
      excerpt: "...remember the ladies, and be more generous and favorable to them than your ancestors. Do not put such unlimited power into the hands of the Husbands."
    },
    { 
      title: "Give Me Liberty or Give Me Death", 
      date: "March 23, 1775", 
      authors: ["Patrick Henry"],
      type: "speech",
      excerpt: "Is life so dear, or peace so sweet, as to be purchased at the price of chains and slavery? Forbid it, Almighty God! I know not what course others may take; but as for me, give me liberty or give me death!"
    },
    { 
      title: "The Constitution of the United States", 
      date: "September 17, 1787", 
      authors: ["Constitutional Convention"],
      type: "founding_document",
      excerpt: "We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity..."
    },
    { 
      title: "Federalist No. 10", 
      date: "November 22, 1787", 
      authors: ["James Madison"],
      type: "essay",
      excerpt: "The inference to which we are brought is, that the causes of faction cannot be removed, and that relief is only to be sought in the means of controlling its effects."
    },
    { 
      title: "The Bill of Rights", 
      date: "September 25, 1789", 
      authors: ["James Madison", "First Congress"],
      type: "founding_document",
      excerpt: "Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble..."
    },
    { 
      title: "From Thomas Jefferson to John Adams", 
      date: "October 28, 1813", 
      authors: ["Thomas Jefferson"],
      type: "letter",
      excerpt: "The whole of government consists in the art of being honest. Only aim to do your duty, and mankind will give you credit where you fail."
    },
  ];

  // Group documents by type
  const documentsByType = documents.reduce((acc, doc) => {
    acc[doc.type] = acc[doc.type] || [];
    acc[doc.type].push(doc);
    return acc;
  }, {});

  // Type display names
  const typeNames = {
    "founding_document": "Founding Documents",
    "pamphlet": "Pamphlets",
    "letter": "Letters",
    "speech": "Speeches",
    "essay": "Essays"
  };

  return (
    <div className="flex-1 p-6 overflow-auto">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Historical Documents</h2>
      
      {Object.keys(documentsByType).map(type => (
        <div key={type} className="mb-8">
          <h3 className="text-lg font-medium text-gray-700 mb-3">{typeNames[type] || type}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {documentsByType[type].map((doc, idx) => (
              <div key={idx} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                <h3 className="font-semibold text-gray-800">{doc.title}</h3>
                <div className="flex items-center mt-2 text-sm text-gray-600">
                  <Calendar className="w-4 h-4 mr-1" />
                  <span>{doc.date}</span>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  <span className="font-medium">Authors: </span>
                  {doc.authors.join(", ")}
                </div>
                <p className="mt-3 text-sm text-gray-700 italic">"{doc.excerpt}"</p>
                <div className="mt-3">
                  <span className="inline-block px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                    {doc.type}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Documents;
