// Test script to verify threshold update functionality
// Run this in the browser console after logging in and creating a training plan

console.log('🧪 Testing Threshold Update Functionality...');

// Test 1: Check if UpdateThresholdModal component is available
if (typeof UpdateThresholdModal !== 'undefined') {
  console.log('✅ UpdateThresholdModal component is available');
} else {
  console.log('❌ UpdateThresholdModal component not found');
}

// Test 2: Check if TrainingPlanInfo has the update threshold button
const trainingPlanInfo = document.querySelector('.training-plan-info');
if (trainingPlanInfo) {
  console.log('✅ Training plan info panel found');
  
  const updateButton = trainingPlanInfo.querySelector('.btn-update-threshold');
  if (updateButton) {
    console.log('✅ Update threshold button found');
    console.log('Button text:', updateButton.textContent);
  } else {
    console.log('❌ Update threshold button not found');
  }
  
  // Check that view calendar button is removed
  const viewCalendarButton = trainingPlanInfo.querySelector('.btn-view-calendar');
  if (viewCalendarButton) {
    console.log('❌ View calendar button still exists (should be removed)');
  } else {
    console.log('✅ View calendar button correctly removed');
  }
} else {
  console.log('❌ Training plan info panel not found');
}

// Test 3: Check if main action button exists only when no active plan
const mainButton = document.querySelector('.main-btn');
if (mainButton) {
  console.log('✅ Main action button found');
  console.log('Button text:', mainButton.textContent);
  
  // Check if it shows "Start Training Plan" (should only exist when no active plan)
  if (mainButton.textContent.includes('Start Training Plan')) {
    console.log('✅ Button correctly shows "Start Training Plan" (no active plan)');
  } else {
    console.log('❌ Button shows unexpected text:', mainButton.textContent);
  }
} else {
  console.log('ℹ️ Main action button not found (user has active plan)');
}

// Test 4: Check layout positioning
const mainLayout = document.querySelector('.main-layout');
if (mainLayout) {
  console.log('✅ Main layout found');
  
  const sidebar = mainLayout.querySelector('.main-sidebar');
  if (sidebar) {
    const computedStyle = window.getComputedStyle(sidebar);
    console.log('✅ Sidebar found');
    console.log('Sidebar margin-left:', computedStyle.marginLeft);
  }
} else {
  console.log('❌ Main layout not found');
}

// Test 5: Check localStorage for token
const token = localStorage.getItem('token');
if (token) {
  console.log('✅ Authentication token found');
} else {
  console.log('❌ No authentication token found - please log in first');
}

console.log('\n🎯 Expected Features:');
console.log('1. Training plan info panel moved further left');
console.log('2. "View Calendar" button removed from info panel');
console.log('3. "Update Threshold" button added to info panel');
console.log('4. Update threshold modal opens with time selectors');
console.log('5. Main button only shows when no active plan exists');
console.log('6. Backend PUT endpoint for threshold updates');

console.log('\n📋 To test threshold updates:');
console.log('1. Click "Update Threshold" button');
console.log('2. Fill in any combination of threshold fields');
console.log('3. Submit and verify API call');
console.log('4. Check that plan info updates automatically');

console.log('\n🎉 Threshold Update Functionality Test Complete!'); 