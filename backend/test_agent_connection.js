/*
 * Test script to verify the agent connection and functionality
 */
async function testAgentConnection() {
  console.log('Testing agent connection and functionality...');

  try {
    // Test the query endpoint with a sample query
    const response = await fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: 'What is ROS 2?',
        max_tokens: 1024  // Free tier limit
      }),
    });

    console.log('Query endpoint status:', response.status);

    if (response.status === 200) {
      const data = await response.json();
      console.log('✅ Agent connection successful!');
      console.log('Response content length:', data.content.length, 'characters');
      console.log('Number of sources:', data.sources.length);
      console.log('Response content preview:', data.content.substring(0, 200) + '...');

      if (data.confidence) {
        console.log('Response confidence:', data.confidence);
      }

      return true;
    } else {
      console.error('❌ Agent returned error:', response.status);
      const errorText = await response.text();
      console.error('Error details:', errorText);
      return false;
    }
  } catch (error) {
    console.error('❌ Network error connecting to agent:', error);
    return false;
  }
}

// Run the test
testAgentConnection();