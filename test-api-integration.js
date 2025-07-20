// Simple test script to verify API integration
// Run with: node test-api-integration.js

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Test with a deployed backend URL if available
const DEPLOYED_BACKEND_URLS = [
  'https://leetcode-video-generator.onrender.com',
  // Add your deployed backend URL here
];

async function testUrl(url) {
  try {
    const response = await fetch(`${url}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000) // 5 second timeout
    });
    return response.ok;
  } catch {
    return false;
  }
}

async function testApiIntegration() {
  console.log('🧪 Testing API Integration...');

  // Try to find a working backend URL
  let workingUrl = null;

  console.log(`\n🔍 Testing backend URLs...`);

  // Test local backend first
  console.log(`Testing local: ${API_BASE_URL}`);
  if (await testUrl(API_BASE_URL)) {
    workingUrl = API_BASE_URL;
    console.log('✅ Local backend is running');
  } else {
    console.log('❌ Local backend not available');
  }

  // Test deployed backends if local isn't available
  if (!workingUrl) {
    for (const url of DEPLOYED_BACKEND_URLS) {
      console.log(`Testing deployed: ${url}`);
      if (await testUrl(url)) {
        workingUrl = url;
        console.log('✅ Deployed backend found');
        break;
      } else {
        console.log('❌ Not available');
      }
    }
  }

  if (!workingUrl) {
    console.log('\n❌ No working backend found!');
    console.log('\n💡 To test the integration:');
    console.log('   1. Start local backend: cd backend && python main.py');
    console.log('   2. Or deploy backend and update DEPLOYED_BACKEND_URLS in this script');
    return;
  }

  console.log(`\n🎯 Using backend: ${workingUrl}`);

  try {
    // Test 1: Health check
    console.log('\n1. Testing health check...');
    const healthResponse = await fetch(`${workingUrl}/health`);

    if (healthResponse.ok) {
      const responseText = await healthResponse.text();
      try {
        const healthData = JSON.parse(responseText);
        console.log('✅ Health check passed:', healthData);
      } catch (e) {
        // Handle non-JSON responses
        console.log('✅ Health check passed (text response):', responseText);
      }
    } else {
      console.log('❌ Health check failed:', healthResponse.status);
      return;
    }

    // Test 2: Video generation
    console.log('\n2. Testing video generation...');
    const videoRequest = {
      problem_title: 'Two Sum',
      language: 'python',
      video_type: 'explanation'
    };

    const videoResponse = await fetch(`${workingUrl}/api/generate-video`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(videoRequest),
    });

    if (videoResponse.ok) {
      const videoData = await videoResponse.json();
      console.log('✅ Video generation request successful:', videoData);
    } else {
      const errorData = await videoResponse.json().catch(() => ({ detail: 'Unknown error' }));
      console.log('❌ Video generation failed:', videoResponse.status, errorData);
    }

    console.log('\n🎉 API integration test completed!');

  } catch (error) {
    console.log('❌ Connection failed:', error.message);
    console.log('\n💡 Make sure your backend is running:');
    console.log('   - For local: cd backend && python main.py');
    console.log('   - For deployed: Update NEXT_PUBLIC_API_URL in .env.local');
  }
}

testApiIntegration();