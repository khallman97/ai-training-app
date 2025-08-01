// Test script to verify training plan info panel integration
// Run this in the browser console after logging in

console.log('🧪 Testing Training Plan Info Panel Integration...');

// Test 1: Check if TrainingPlanInfo component is available
if (typeof TrainingPlanInfo !== 'undefined') {
  console.log('✅ TrainingPlanInfo component is available');
} else {
  console.log('❌ TrainingPlanInfo component not found');
}

// Test 2: Check if MainScreen has the new layout
const mainScreen = document.querySelector('.main-content-wrapper');
if (mainScreen) {
  console.log('✅ MainScreen component is rendered');
  
  // Check for the new layout structure
  const mainLayout = mainScreen.querySelector('.main-layout');
  if (mainLayout) {
    console.log('✅ Main layout structure found');
    
    // Check for sidebar
    const sidebar = mainLayout.querySelector('.main-sidebar');
    if (sidebar) {
      console.log('✅ Sidebar found');
      
      // Check for training plan info
      const trainingPlanInfo = sidebar.querySelector('.training-plan-info');
      if (trainingPlanInfo) {
        console.log('✅ Training plan info panel found');
        
        // Check if it shows no plan state
        const noPlan = trainingPlanInfo.querySelector('.no-plan');
        if (noPlan) {
          console.log('✅ No plan state displayed correctly');
        } else {
          console.log('ℹ️ Plan info displayed (user has active plan)');
        }
      } else {
        console.log('❌ Training plan info panel not found in sidebar');
      }
    } else {
      console.log('❌ Sidebar not found');
    }
    
    // Check for center area
    const center = mainLayout.querySelector('.main-center');
    if (center) {
      console.log('✅ Center area found');
      
      // Check for button
      const button = center.querySelector('.main-btn');
      if (button) {
        console.log('✅ Action button found');
        console.log('Button text:', button.textContent);
      } else {
        console.log('❌ Action button not found');
      }
    } else {
      console.log('❌ Center area not found');
    }
  } else {
    console.log('❌ Main layout structure not found');
  }
} else {
  console.log('❌ MainScreen component not found');
}

// Test 3: Check localStorage for token
const token = localStorage.getItem('token');
if (token) {
  console.log('✅ Authentication token found');
} else {
  console.log('❌ No authentication token found - please log in first');
}

console.log('\n🎯 Expected Layout:');
console.log('┌─────────────────────────────────────────┐');
console.log('│ Navigation Bar                          │');
console.log('├─────────────┬───────────────────────────┤');
console.log('│ Training    │ Calendar Area             │');
console.log('│ Plan Info   │ (Center focus)            │');
console.log('│ (Left)      │                           │');
console.log('│             │                           │');
console.log('└─────────────┴───────────────────────────┘');

console.log('\n📋 Features to test:');
console.log('1. Training plan info displays on left side');
console.log('2. Calendar area remains centered');
console.log('3. Responsive design on mobile');
console.log('4. Plan details show correctly when plan exists');
console.log('5. No plan state shows when no plan exists');

console.log('\n🎉 Training Plan Info Panel Integration Test Complete!'); 