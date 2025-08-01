# Training Plan System Design Document

## 🎯 **Overview**

This document outlines the design for an AI-powered training plan system that generates personalized workout plans using LLM integration, with efficient caching and dynamic adaptation based on user performance.

## 🏗️ **System Architecture**

### **Core Components**
1. **Training Plan Generator** - LLM-powered plan creation
2. **Generic Caching System** - Efficient template reuse
3. **4-Week Block System** - Dynamic training blocks
4. **Workout Upload & Analysis** - Performance tracking
5. **Adaptive Planning** - Performance-based modifications

### **Key Principles**
- **Efficiency**: Minimize LLM calls through intelligent caching
- **Flexibility**: Support any training plan type and user level
- **Personalization**: Adapt plans based on user performance and preferences
- **Scalability**: Handle multiple users and plan types efficiently

## 🗄️ **Data Structure**

### **Core Tables**

#### **1. Training Plan Cache**
```sql
training_plan_cache (
  id SERIAL PRIMARY KEY,
  cache_key VARCHAR(255) UNIQUE NOT NULL,
  request_data JSONB NOT NULL,
  response_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  last_used_at TIMESTAMP DEFAULT NOW(),
  usage_count INTEGER DEFAULT 1,
  is_active BOOLEAN DEFAULT TRUE
)
```

#### **2. User Training Plans**
```sql
training_plans (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  cache_key VARCHAR(255) REFERENCES training_plan_cache(cache_key),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL, -- running, cycling, triathlon
  start_date DATE NOT NULL,
  event_date DATE NOT NULL,
  skill_level VARCHAR(20) NOT NULL, -- beginner, intermediate, master
  long_days JSONB NOT NULL, -- array of days
  performance_metrics JSONB, -- thresholds and other metrics
  current_phase VARCHAR(50), -- base, build, peak, taper
  current_block_week INTEGER, -- current week in 4-week block
  status VARCHAR(20) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

#### **3. Training Blocks**
```sql
training_blocks (
  id SERIAL PRIMARY KEY,
  training_plan_id INTEGER REFERENCES training_plans(id),
  phase_name VARCHAR(50) NOT NULL, -- base, build, peak, taper
  block_number INTEGER NOT NULL, -- 1, 2, 3, etc.
  start_week INTEGER NOT NULL,
  end_week INTEGER NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  status VARCHAR(20) DEFAULT 'active',
  generated_at TIMESTAMP DEFAULT NOW(),
  llm_version VARCHAR(50),
  is_cached BOOLEAN DEFAULT FALSE
)
```

#### **4. Block Workouts**
```sql
block_workouts (
  id SERIAL PRIMARY KEY,
  training_block_id INTEGER REFERENCES training_blocks(id),
  week_number INTEGER NOT NULL,
  day_number INTEGER NOT NULL,
  workout_type VARCHAR(50) NOT NULL, -- run, bike, swim, strength, rest
  title VARCHAR(255) NOT NULL,
  description TEXT,
  target_duration INTEGER, -- minutes
  target_distance DECIMAL(8,2), -- km
  target_intensity VARCHAR(50), -- zone_1, zone_2, etc.
  instructions TEXT,
  created_at TIMESTAMP DEFAULT NOW()
)
```

#### **5. User Workouts**
```sql
user_workouts (
  id SERIAL PRIMARY KEY,
  training_plan_id INTEGER REFERENCES training_plans(id),
  block_workout_id INTEGER REFERENCES block_workouts(id),
  planned_date DATE NOT NULL,
  actual_date DATE,
  status VARCHAR(20) DEFAULT 'planned', -- planned, completed, skipped
  user_notes TEXT,
  performance_data JSONB, -- workout metrics
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

#### **6. Workout Metrics**
```sql
workout_metrics (
  id SERIAL PRIMARY KEY,
  user_workout_id INTEGER REFERENCES user_workouts(id),
  metric_type VARCHAR(50) NOT NULL, -- heart_rate, pace, power, location
  metric_name VARCHAR(100) NOT NULL,
  metric_value DECIMAL(10,4),
  metric_unit VARCHAR(20),
  timestamp TIMESTAMP,
  data_source VARCHAR(50), -- garmin_connect, coros, manual
  raw_data JSONB, -- array of time-series data
  created_at TIMESTAMP DEFAULT NOW()
)
```

## 🔄 **System Workflow**

### **Training Plan Creation Flow**

#### **Step 1: Cache Check**
```
User creates plan → Generate cache key from request parameters
→ Check if cache_key exists and is_active
→ If exists: Use cached response and increment usage_count
→ If not: Proceed to LLM generation
```

#### **Step 2: LLM Generation (if needed)**
```
Generate plan structure with LLM:
- Phase breakdown (Base, Build, Peak, Taper)
- Phase durations and goals
- First 4-week training block details
→ Cache response for future use
```

#### **Step 3: Plan Personalization**
```
Check user thresholds and preferences:
- If no thresholds: Adapt first week for threshold testing
- If has thresholds: Calculate zone-based targets
- Adjust workouts based on user's long training days
```

### **Training Block Management**

#### **4-Week Block Structure**
- **Weeks 1-3**: Load weeks (increasing intensity/volume)
- **Week 4**: Recovery week (reduced intensity/volume)
- **Block Types**: Base, Build, Peak, Taper phases

#### **Block Generation Flow**
```
User completes current block → Analyze performance data
→ Generate next 4-week block based on:
- Current phase goals
- Performance trends
- Missed workouts
- User feedback
```

## 🤖 **LLM Integration Strategy**

### **LLM Call Types**

#### **1. Template Generation (Cached)**
```
Input: Plan type, skill level, duration, event type
Output: Phase breakdown and first 4-week block
Frequency: Once per unique plan combination
```

#### **2. Block Personalization (Cached)**
```
Input: Template + user thresholds/preferences
Output: Personalized first block
Frequency: Once per unique user profile
```

#### **3. Performance Adaptation (Dynamic)**
```
Input: Current performance + phase goals
Output: Modified remaining workouts in current block
Frequency: As needed based on performance
```

#### **4. Next Block Generation (Dynamic)**
```
Input: Phase goals + performance data + user progress
Output: Next 4-week training block
Frequency: Every 4 weeks
```

### **LLM Efficiency Benefits**
- **Template Generation**: 1 call per plan type (cached)
- **First Block**: 1 call per plan type × user profile variations (cached)
- **Adaptations**: Only when needed (performance-based)
- **Subsequent Blocks**: 1 call per 4 weeks

**Total LLM calls per user per 12-week plan**: ~4-6 calls vs. traditional 84 calls

## 📊 **Caching System**

### **Cache Key Generation**
```python
def generate_cache_key(request_data):
    # Normalize request data for consistent caching
    normalized_data = {
        "plan_type": request_data.get("plan_type"),
        "skill_level": request_data.get("skill_level"),
        "duration_weeks": request_data.get("duration_weeks"),
        "has_thresholds": request_data.get("has_thresholds", False),
        "event_type": request_data.get("event_type")
    }
    
    # Create hash for cache key
    request_string = json.dumps(normalized_data, sort_keys=True)
    return hashlib.md5(request_string.encode()).hexdigest()
```

### **Cache Management**
- **Automatic Creation**: Cache created on first LLM generation
- **Automatic Usage**: Cache used for all similar requests
- **Manual Deletion**: Only by admin/backend access
- **Usage Tracking**: Monitor cache effectiveness

### **Cache Benefits**
- **Efficiency**: 90% reduction in LLM calls
- **Consistency**: Same plan structure for similar users
- **Speed**: Instant plan generation for cached templates
- **Cost**: Minimal LLM token usage

## 🎯 **Implementation Phases**

### **Phase 1: Foundation & Caching**
**Duration**: 2-3 weeks
**Goals**:
- Build generic caching system
- Create LLM integration service
- Implement basic plan generation
- Build cache management interface

**Deliverables**:
- Training plan cache table
- LLM service for plan generation
- Cache key generation and management
- Basic plan creation API

### **Phase 2: 4-Week Block System**
**Duration**: 2-3 weeks
**Goals**:
- Implement 4-week training blocks
- Build block completion tracking
- Create next block generation logic
- Add performance-based adaptations

**Deliverables**:
- Training blocks and block workouts tables
- Block scheduling system
- Block completion tracking
- Next block generation API

### **Phase 3: Workout Upload & Analysis**
**Duration**: 3-4 weeks
**Goals**:
- Build workout upload infrastructure
- Integrate with fitness platforms (Garmin, Coros)
- Create workout metrics storage
- Implement performance analysis

**Deliverables**:
- Workout upload API
- Platform integrations (Garmin, Coros)
- Workout metrics storage
- Performance analysis engine

### **Phase 4: Dynamic Adaptations**
**Duration**: 2-3 weeks
**Goals**:
- Implement performance-based adaptations
- Build LLM-powered insights
- Create adaptive plan modifications
- Add user feedback integration

**Deliverables**:
- Performance-based workout adaptations
- LLM-powered training insights
- Adaptive plan modification system
- User feedback integration

### **Phase 5: Advanced Features**
**Duration**: 2-3 weeks
**Goals**:
- Add advanced analytics
- Implement goal tracking
- Create progress reporting
- Build admin management tools

**Deliverables**:
- Advanced analytics dashboard
- Goal tracking system
- Progress reporting
- Admin management interface

## 🔧 **Technical Implementation**

### **Zone Calculation Service**
```python
class ZoneCalculator:
    def calculate_running_zones(self, threshold_pace):
        """Calculate running zones based on threshold pace"""
        threshold_seconds = self.parse_pace_to_seconds(threshold_pace)
        
        return {
            'zone_1': threshold_seconds * 1.25,  # < 80%
            'zone_2': threshold_seconds * 1.12,  # 80-89%
            'zone_3': threshold_seconds * 1.05,  # 90-99%
            'zone_4': threshold_seconds * 0.95,  # 100-109%
            'zone_5': threshold_seconds * 0.85   # > 110%
        }
    
    def calculate_cycling_zones(self, ftp):
        """Calculate cycling zones based on FTP"""
        return {
            'zone_1': ftp * 0.55,  # < 55%
            'zone_2': ftp * 0.75,  # 55-75%
            'zone_3': ftp * 0.90,  # 76-90%
            'zone_4': ftp * 1.05,  # 91-105%
            'zone_5': ftp * 1.20   # > 105%
        }
```

### **Workout Upload Service**
```python
class WorkoutUploadService:
    def __init__(self):
        self.supported_platforms = {
            'garmin_connect': GarminConnectAPI(),
            'coros': CorosAPI(),
            'strava': StravaAPI(),
            'manual': ManualEntryAPI()
        }
    
    def upload_workout(self, platform, workout_data):
        """Upload workout from supported platform"""
        if platform in self.supported_platforms:
            return self.supported_platforms[platform].process_workout(workout_data)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
```

### **Performance Analysis Engine**
```python
class PerformanceAnalyzer:
    def analyze_workout_performance(self, user_workout_id):
        """Analyze completed workout performance"""
        metrics = self.get_workout_metrics(user_workout_id)
        
        return {
            'average_heart_rate': self.calculate_avg_hr(metrics),
            'peak_heart_rate': self.calculate_peak_hr(metrics),
            'average_pace': self.calculate_avg_pace(metrics),
            'total_distance': self.calculate_total_distance(metrics),
            'calories_burned': self.calculate_calories(metrics),
            'zone_distribution': self.calculate_hr_zones(metrics)
        }
```

## 📈 **Performance Considerations**

### **Database Optimization**
- Index on `cache_key` for fast cache lookups
- Index on `planned_date` and `actual_date` for calendar queries
- Partition `workout_metrics` by date for large datasets
- Use JSONB for flexible metric storage

### **Caching Strategy**
- Cache training templates indefinitely
- Cache first blocks for common combinations
- Implement cache warming for popular plans
- Monitor cache hit rates for optimization

### **LLM Cost Management**
- Use smaller context windows for block generation
- Implement request batching where possible
- Monitor token usage per request
- Set rate limits to prevent abuse

## 🔒 **Security & Privacy**

### **Data Protection**
- Encrypt sensitive user data
- Implement proper authentication and authorization
- Secure API endpoints with rate limiting
- Regular security audits

### **User Privacy**
- Anonymize performance data for analytics
- Allow users to delete their data
- Implement data retention policies
- Comply with GDPR/privacy regulations

## 📊 **Monitoring & Analytics**

### **System Metrics**
- Cache hit rates and performance
- LLM call frequency and costs
- API response times
- Error rates and types

### **User Analytics**
- Most popular plan types
- User engagement and retention
- Performance improvement trends
- Feature usage patterns

### **Business Metrics**
- User acquisition and growth
- Plan completion rates
- User satisfaction scores
- Revenue and cost analysis

## 🚀 **Future Enhancements**

### **Advanced Features**
- Multi-sport training plans
- Team/group training features
- Integration with coaching platforms
- Advanced performance analytics

### **AI Improvements**
- More sophisticated LLM prompts
- Better performance prediction
- Personalized training recommendations
- Injury prevention algorithms

### **Platform Expansions**
- Additional fitness platform integrations
- Wearable device support
- Mobile app development
- API for third-party integrations

---

**Document Version**: 1.0  
**Last Updated**: January 2024  
**Next Review**: February 2024 