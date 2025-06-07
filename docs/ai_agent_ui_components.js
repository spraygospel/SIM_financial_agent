// ============================================================================
// AI AGENT UI/UX COMPONENTS FOR MYSQL QUERY SYSTEM
// ============================================================================
// This file contains all React components for the AI Agent interface
// Features: Real-time monitoring, context management, fallback tracking, 
// performance analytics, session control, and transparent data display
// ============================================================================

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell } from 'recharts';

// ============================================================================
// MAIN DASHBOARD COMPONENT
// ============================================================================
const AIAgentDashboard = () => {
  // State management for all UI components
  const [agentState, setAgentState] = useState({
    isProcessing: false,
    currentStep: 'idle',
    contextUsage: 78,
    totalTokens: 15240,
    maxTokens: 19500,
    processTimings: {},
    queryResults: [],
    narrative: '',
    warnings: [],
    sessionId: 'session_2024_001',
    queryCount: 7,
    successRate: 85.7
  });

  return (
    <div className="ai-agent-dashboard">
      {/* Header with Session Management */}
      <SessionHeader agentState={agentState} setAgentState={setAgentState} />
      
      {/* Main Content Area */}
      <div className="dashboard-content">
        {/* Left Panel: Monitoring & Controls */}
        <div className="left-panel">
          <ContextUsageMeter agentState={agentState} />
          <ProcessMonitor agentState={agentState} />
          <PerformanceAnalytics agentState={agentState} />
          <FallbackTracker agentState={agentState} />
        </div>
        
        {/* Right Panel: Query Interface & Results */}
        <div className="right-panel">
          <QueryInterface agentState={agentState} setAgentState={setAgentState} />
          <ResultsDisplay agentState={agentState} />
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// SESSION HEADER COMPONENT
// ============================================================================
// Displays session info, context usage, and session management controls
const SessionHeader = ({ agentState, setAgentState }) => {
  
  // Handle new chat creation - resets state but can preserve schema knowledge
  const handleNewChat = () => {
    const preserveSchema = window.confirm(
      "Keep database schema knowledge? (saves 3s reload time)"
    );
    
    setAgentState(prev => ({
      ...prev,
      sessionId: `session_${Date.now()}`,
      queryCount: 0,
      queryResults: [],
      narrative: '',
      warnings: [],
      contextUsage: preserveSchema ? 45 : 5, // Schema knowledge ~45% of context
      totalTokens: preserveSchema ? 8950 : 500
    }));
  };

  // Context optimization - removes old data to free up tokens
  const handleOptimizeContext = () => {
    setAgentState(prev => ({
      ...prev,
      contextUsage: Math.max(35, prev.contextUsage - 25), // Reduce by ~25%
      totalTokens: Math.max(6800, prev.totalTokens - 4500)
    }));
  };

  return (
    <header className="session-header">
      <div className="session-info">
        <h1>🤖 AI MySQL Query Agent</h1>
        <div className="session-details">
          <span>Session: {agentState.sessionId}</span>
          <span>Queries: {agentState.queryCount}</span>
          <span>Success Rate: {agentState.successRate}%</span>
        </div>
      </div>
      
      {/* Context Usage Indicator */}
      <div className="context-indicator">
        <div className="context-bar">
          <div 
            className={`context-fill ${agentState.contextUsage > 80 ? 'warning' : 'normal'}`}
            style={{ width: `${agentState.contextUsage}%` }}
          />
        </div>
        <span>{agentState.contextUsage}% Context Used</span>
      </div>
      
      {/* Session Controls */}
      <div className="session-controls">
        <button onClick={handleOptimizeContext} className="btn-optimize">
          🧹 Optimize Context
        </button>
        <button onClick={handleNewChat} className="btn-new-chat">
          🆕 New Chat
        </button>
      </div>
    </header>
  );
};

// ============================================================================
// CONTEXT USAGE METER COMPONENT  
// ============================================================================
// Shows detailed token usage breakdown and optimization suggestions
const ContextUsageMeter = ({ agentState }) => {
  
  // Calculate token breakdown for visualization
  const tokenBreakdown = [
    { name: 'Schema Knowledge', value: 8950, color: '#8884d8', percentage: 58.7 },
    { name: 'Query Results', value: 4780, color: '#82ca9d', percentage: 31.4 },
    { name: 'Conversation', value: 1465, color: '#ffc658', percentage: 9.6 },
    { name: 'System Context', value: 45, color: '#ff7c7c', percentage: 0.3 }
  ];

  // Determine warning level based on usage
  const getUsageWarning = (usage) => {
    if (usage > 85) return { level: 'critical', message: '🚨 Context nearly full - cleanup required' };
    if (usage > 75) return { level: 'warning', message: '⚠️ Context approaching limit' };
    return { level: 'normal', message: '✅ Context usage healthy' };
  };

  const warning = getUsageWarning(agentState.contextUsage);

  return (
    <div className="context-usage-meter">
      <h3>🧠 Context Window Usage</h3>
      
      {/* Main Usage Bar */}
      <div className="usage-display">
        <div className="usage-bar-container">
          <div 
            className={`usage-bar ${warning.level}`}
            style={{ width: `${agentState.contextUsage}%` }}
          />
          <span className="usage-text">
            {agentState.totalTokens.toLocaleString()} / {agentState.maxTokens.toLocaleString()} tokens
          </span>
        </div>
        <div className={`usage-warning ${warning.level}`}>
          {warning.message}
        </div>
      </div>

      {/* Token Breakdown */}
      <div className="token-breakdown">
        <h4>Token Distribution:</h4>
        {tokenBreakdown.map((item, index) => (
          <div key={index} className="breakdown-item">
            <div 
              className="breakdown-color" 
              style={{ backgroundColor: item.color }}
            />
            <span className="breakdown-label">{item.name}</span>
            <span className="breakdown-value">
              {item.value.toLocaleString()} ({item.percentage}%)
            </span>
          </div>
        ))}
      </div>

      {/* Optimization Suggestions */}
      <div className="optimization-suggestions">
        <h4>💡 Optimization Opportunities:</h4>
        <ul>
          <li>📁 Archive old query results: -2,400 tokens</li>
          <li>🗜️ Compress conversation history: -730 tokens</li>
          <li>💾 Cache stable schema info: -1,200 tokens</li>
          <li><strong>Total Recoverable: 4,330 tokens (28% reduction)</strong></li>
        </ul>
      </div>
    </div>
  );
};

// ============================================================================
// PROCESS MONITOR COMPONENT
// ============================================================================
// Shows real-time progress of agent workflow with checkmarks and timing
const ProcessMonitor = ({ agentState }) => {
  
  // Define workflow steps with their status and timing
  const workflowSteps = [
    { 
      id: 1, 
      name: 'Understanding User Query', 
      status: 'completed', 
      duration: 0.8,
      description: 'Parsing intent and extracting entities'
    },
    { 
      id: 2, 
      name: 'Consulting Schema Knowledge', 
      status: 'completed', 
      duration: 1.6,
      description: 'Searching GraphDB for relevant tables'
    },
    { 
      id: 3, 
      name: 'Planning SQL Execution', 
      status: 'completed', 
      duration: 2.1,
      description: 'Creating query plan and response template'
    },
    { 
      id: 4, 
      name: 'Executing Database Queries', 
      status: agentState.isProcessing ? 'in_progress' : 'completed', 
      duration: 2.3,
      description: 'Running SQL queries with fallback handling'
    },
    { 
      id: 5, 
      name: 'Validating Results', 
      status: agentState.isProcessing ? 'pending' : 'completed', 
      duration: 0.4,
      description: 'Checking data quality and consistency'
    },
    { 
      id: 6, 
      name: 'Generating Response', 
      status: agentState.isProcessing ? 'pending' : 'completed', 
      duration: 1.9,
      description: 'Replacing placeholders and formatting output'
    }
  ];

  // Get status icon for each step
  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return '✅';
      case 'in_progress': return '🔄';
      case 'failed': return '❌';
      case 'pending': return '⏳';
      default: return '⚪';
    }
  };

  // Get status class for styling
  const getStatusClass = (status) => {
    return `step-${status}`;
  };

  return (
    <div className="process-monitor">
      <h3>⚙️ Agent Process Monitor</h3>
      
      {/* Overall Progress */}
      <div className="overall-progress">
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ 
              width: `${(workflowSteps.filter(s => s.status === 'completed').length / workflowSteps.length) * 100}%` 
            }}
          />
        </div>
        <span>
          {workflowSteps.filter(s => s.status === 'completed').length} / {workflowSteps.length} steps completed
        </span>
      </div>

      {/* Step-by-step Progress */}
      <div className="workflow-steps">
        {workflowSteps.map((step) => (
          <div key={step.id} className={`workflow-step ${getStatusClass(step.status)}`}>
            <div className="step-header">
              <span className="step-icon">{getStatusIcon(step.status)}</span>
              <span className="step-number">{step.id}.</span>
              <span className="step-name">{step.name}</span>
              {step.status === 'completed' && (
                <span className="step-duration">[{step.duration}s]</span>
              )}
            </div>
            <div className="step-description">{step.description}</div>
            {step.status === 'in_progress' && (
              <div className="step-progress">
                <div className="progress-spinner"></div>
                <span>Processing...</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Current Status */}
      <div className="current-status">
        {agentState.isProcessing ? (
          <div className="status-processing">
            🔄 <strong>Current Status:</strong> Fetching customer payment data...
          </div>
        ) : (
          <div className="status-complete">
            ✅ <strong>Status:</strong> All processes completed successfully
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// PERFORMANCE ANALYTICS COMPONENT
// ============================================================================
// Shows detailed timing breakdown and performance metrics
const PerformanceAnalytics = ({ agentState }) => {
  
  // Sample performance data for visualization
  const performanceData = [
    { component: 'LLM API Calls', time: 4.1, percentage: 36.6, color: '#8884d8' },
    { component: 'MySQL Query', time: 2.3, percentage: 20.5, color: '#82ca9d' },
    { component: 'Reasoning', time: 1.9, percentage: 17.0, color: '#ffc658' },
    { component: 'GraphDB Query', time: 1.6, percentage: 14.3, color: '#ff7c7c' },
    { component: 'Data Processing', time: 0.8, percentage: 7.1, color: '#8dd1e1' },
    { component: 'Formatting', time: 0.5, percentage: 4.5, color: '#d084d0' }
  ];

  const totalTime = performanceData.reduce((sum, item) => sum + item.time, 0);

  return (
    <div className="performance-analytics">
      <h3>⚡ Performance Analytics</h3>
      
      {/* Total Time Display */}
      <div className="total-time">
        <div className="time-display">
          <span className="time-value">🕐 {totalTime.toFixed(1)}s</span>
          <span className="time-label">Total Processing Time</span>
        </div>
        <div className={`performance-rating ${totalTime < 10 ? 'excellent' : totalTime < 15 ? 'good' : 'slow'}`}>
          {totalTime < 10 ? '🚀 Excellent' : totalTime < 15 ? '✅ Good' : '⚠️ Slow'}
        </div>
      </div>

      {/* Component Breakdown */}
      <div className="component-breakdown">
        <h4>Component Timing Breakdown:</h4>
        {performanceData.map((item, index) => (
          <div key={index} className="component-item">
            <div className="component-info">
              <div 
                className="component-color"
                style={{ backgroundColor: item.color }}
              />
              <span className="component-name">{item.component}</span>
            </div>
            <div className="component-metrics">
              <span className="component-time">{item.time}s</span>
              <span className="component-percentage">({item.percentage}%)</span>
            </div>
            <div className="component-bar">
              <div 
                className="component-fill"
                style={{ 
                  width: `${item.percentage}%`,
                  backgroundColor: item.color 
                }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Performance Insights */}
      <div className="performance-insights">
        <h4>🎯 Performance Insights:</h4>
        <ul>
          <li>🐌 <strong>Bottleneck:</strong> LLM API calls (4.1s avg)</li>
          <li>⚡ <strong>Fastest:</strong> Data formatting (0.5s avg)</li>
          <li>💡 <strong>Optimization:</strong> Cache schema knowledge (-1.2s potential)</li>
          <li>📊 <strong>Target:</strong> &lt;10s total time (Current: {totalTime.toFixed(1)}s)</li>
        </ul>
      </div>

      {/* Session Performance Stats */}
      <div className="session-stats">
        <h4>📈 Session Performance:</h4>
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-value">{agentState.successRate}%</span>
            <span className="stat-label">Success Rate</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">8.4s</span>
            <span className="stat-label">Avg Response</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{agentState.queryCount}</span>
            <span className="stat-label">Total Queries</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">95</span>
            <span className="stat-label">Quality Score</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// FALLBACK TRACKER COMPONENT
// ============================================================================
// Shows fallback attempts, retry logic, and recovery explanations
const FallbackTracker = ({ agentState }) => {
  
  // Sample fallback data - in real app this comes from agent state
  const fallbackAttempts = [
    {
      attempt: 1,
      status: 'failed',
      query: "SELECT * FROM customer_payments WHERE...",
      error: "Table 'customer_payments' not found",
      strategy: "Searching alternative table names",
      duration: 0.8
    },
    {
      attempt: 2,
      status: 'failed', 
      query: "SELECT * FROM payments WHERE date_range...",
      error: "No data for specified date range",
      strategy: "Expanding date range to find nearest data",
      duration: 1.2
    },
    {
      attempt: 3,
      status: 'success',
      query: "SELECT customers.name, invoices.amount...",
      error: null,
      strategy: "Using invoice-payment LEFT JOIN approach",
      duration: 2.3
    }
  ];

  const getAttemptIcon = (status) => {
    switch (status) {
      case 'success': return '✅';
      case 'failed': return '❌'; 
      case 'in_progress': return '🔄';
      default: return '⚪';
    }
  };

  const hasAnyFallbacks = fallbackAttempts.length > 1;

  return (
    <div className="fallback-tracker">
      <h3>🔄 Fallback & Retry Monitor</h3>
      
      {!hasAnyFallbacks ? (
        <div className="no-fallbacks">
          <div className="success-message">
            ✅ <strong>Primary query successful</strong> - No fallbacks needed
          </div>
        </div>
      ) : (
        <>
          {/* Fallback Summary */}
          <div className="fallback-summary">
            <div className="summary-stats">
              <span>Attempts: {fallbackAttempts.length}/3</span>
              <span>Final Status: {fallbackAttempts[fallbackAttempts.length - 1].status === 'success' ? '✅ Success' : '❌ Failed'}</span>
            </div>
          </div>

          {/* Detailed Attempt Log */}
          <div className="attempt-log">
            {fallbackAttempts.map((attempt, index) => (
              <div key={index} className={`attempt-item ${attempt.status}`}>
                <div className="attempt-header">
                  <span className="attempt-icon">{getAttemptIcon(attempt.status)}</span>
                  <span className="attempt-label">Attempt #{attempt.attempt}</span>
                  <span className="attempt-duration">{attempt.duration}s</span>
                </div>
                
                <div className="attempt-details">
                  <div className="query-attempt">
                    <strong>Query:</strong> 
                    <code>{attempt.query.length > 50 ? attempt.query.substring(0, 50) + '...' : attempt.query}</code>
                  </div>
                  
                  {attempt.error && (
                    <div className="attempt-error">
                      <strong>Error:</strong> {attempt.error}
                    </div>
                  )}
                  
                  <div className="attempt-strategy">
                    <strong>Strategy:</strong> {attempt.strategy}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Agent Reasoning Explanation */}
          <div className="agent-reasoning">
            <h4>🤖 Agent Reasoning:</h4>
            <div className="reasoning-explanation">
              <p>I encountered issues with the initial approach, but successfully recovered using fallback strategies:</p>
              <ul>
                <li>✓ Consulted GraphDB for alternative table structures</li>
                <li>✓ Reconstructed business logic using available data</li>
                <li>✓ Validated results maintain data integrity</li>
              </ul>
              <p><strong>Result:</strong> Same business meaning achieved through different technical approach.</p>
            </div>
          </div>
        </>
      )}
      
      {/* Learning & Optimization */}
      <div className="learning-info">
        <h4>📚 Agent Learning:</h4>
        <p>Successful fallback patterns are saved for future similar queries to improve performance.</p>
      </div>
    </div>
  );
};

// ============================================================================
// QUERY INTERFACE COMPONENT
// ============================================================================
// Main query input interface with real-time status updates
const QueryInterface = ({ agentState, setAgentState }) => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Handle query submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setAgentState(prev => ({ ...prev, isProcessing: true }));

    // Simulate API call to agent
    try {
      // In real implementation, this would be an API call to your FastAPI backend
      setTimeout(() => {
        setAgentState(prev => ({
          ...prev,
          isProcessing: false,
          queryCount: prev.queryCount + 1,
          contextUsage: Math.min(95, prev.contextUsage + Math.random() * 15),
          totalTokens: prev.totalTokens + Math.floor(Math.random() * 2000) + 500
        }));
        setIsLoading(false);
        setQuery('');
      }, 3000);
    } catch (error) {
      console.error('Query failed:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className="query-interface">
      <h3>💬 Query Interface</h3>
      
      {/* Query Input Form */}
      <form onSubmit={handleSubmit} className="query-form">
        <div className="input-group">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask me about your data... (e.g., 'Show me customers who haven't paid', 'Sales data for January 2023')"
            className="query-input"
            rows={3}
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className={`query-submit ${isLoading ? 'loading' : ''}`}
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? '🔄 Processing...' : '🚀 Ask Agent'}
          </button>
        </div>
      </form>

      {/* Query Suggestions */}
      <div className="query-suggestions">
        <h4>💡 Try these queries:</h4>
        <div className="suggestion-buttons">
          <button 
            onClick={() => setQuery("Show me customers who haven't paid their invoices")}
            className="suggestion-btn"
          >
            Customer Aging Report
          </button>
          <button 
            onClick={() => setQuery("Total sales for January 2023")}
            className="suggestion-btn"
          >
            Monthly Sales
          </button>
          <button 
            onClick={() => setQuery("List employees with their gamification scores")}
            className="suggestion-btn"
          >
            Employee Performance
          </button>
          <button 
            onClick={() => setQuery("Top 5 selling products this year")}
            className="suggestion-btn"
          >
            Product Analysis
          </button>
        </div>
      </div>

      {/* Recent Queries */}
      <div className="recent-queries">
        <h4>📋 Recent Queries:</h4>
        <div className="query-history">
          <div className="history-item">
            <span className="history-query">Customer payment status</span>
            <span className="history-time">2 minutes ago</span>
            <span className="history-status success">✅</span>
          </div>
          <div className="history-item">
            <span className="history-query">Sales data Q1 2023</span>
            <span className="history-time">5 minutes ago</span>
            <span className="history-status success">✅</span>
          </div>
          <div className="history-item">
            <span className="history-query">Employee list with scores</span>
            <span className="history-time">8 minutes ago</span>
            <span className="history-status failed">❌</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// RESULTS DISPLAY COMPONENT  
// ============================================================================
// Shows raw data table, narrative analysis, and validation warnings
const ResultsDisplay = ({ agentState }) => {
  
  // Sample query results data
  const sampleResults = [
    {
      "Customer Name": "PT ABC Corp",
      "Invoice": "INV-001", 
      "Invoice Amount": "Rp 15.000.000",
      "Paid": "Rp 0",
      "Outstanding": "Rp 15.000.000", 
      "Due Date": "15 Jan 2023",
      "Days Overdue": "45 hari"
    },
    {
      "Customer Name": "CV XYZ Trading",
      "Invoice": "INV-002",
      "Invoice Amount": "Rp 8.500.000", 
      "Paid": "Rp 0",
      "Outstanding": "Rp 8.500.000",
      "Due Date": "20 Jan 2023",
      "Days Overdue": "40 hari"
    },
    {
      "Customer Name": "PT DEF Industries", 
      "Invoice": "INV-003",
      "Invoice Amount": "Rp 12.000.000",
      "Paid": "Rp 6.000.000",
      "Outstanding": "Rp 6.000.000",
      "Due Date": "25 Jan 2023",
      "Days Overdue": "35 hari"
    }
  ];

  // Sample narrative response
  const sampleNarrative = `📊 **Customer Outstanding Report**

**Summary:**
- Total Customer dengan Outstanding: 3 customer
- Total Outstanding Amount: Rp 29.500.000  
- Rata-rata Days Overdue: 40 hari

**Analisis Risiko:**
Customer dengan risiko tertinggi adalah PT ABC Corp dengan outstanding Rp 15.000.000 yang telah overdue selama 45 hari.

**Rekomendasi:**
1. Follow up prioritas untuk PT ABC Corp (100% outstanding)
2. Monitoring ketat untuk CV XYZ Trading (100% outstanding)  
3. PT DEF Industries menunjukkan partial payment, perlu follow up untuk sisanya

Rata-rata days overdue 40 hari mengindikasikan perlu perbaikan dalam collection process.`;

  // Sample validation warnings
  const sampleWarnings = [
    { type: 'info', message: 'ℹ️ Note: 1 invoice over Rp 10M detected (normal for enterprise customers)' },
    { type: 'success', message: '✅ All validations passed' },
    { type: 'info', message: '📅 Report generated: 1 Mar 2023, 14:30 WIB' }
  ];

  // Export function for data table
  const handleExport = (format) => {
    console.log(`Exporting data as ${format}`);
    // In real implementation, would convert data and trigger download
  };

  return (
    <div className="results-display">
      <h3>📊 Query Results</h3>
      
      {/* Executive Summary Cards */}
      <div className="executive-summary">
        <div className="summary-cards">
          <div className="summary-card highlight">
            <span className="card-value">Rp 29.500.000</span>
            <span className="card-label">Total Outstanding</span>
          </div>
          <div className="summary-card">
            <span className="card-value">3</span>
            <span className="card-label">Customers</span>
          </div>
          <div className="summary-card">
            <span className="card-value">40</span>
            <span className="card-label">Avg Days Overdue</span>
          </div>
          <div className="summary-card warning">
            <span className="card-value">95/100</span>
            <span className="card-label">Quality Score</span>
          </div>
        </div>
      </div>

      {/* Raw Data Table */}
      <div className="data-table-section">
        <div className="table-header">
          <h4>📋 Raw Data Table (Retrieved in 2.3s)</h4>
          <div className="table-controls">
            <span className="table-info">Showing 3 of 3 results • Quality Score: 95%</span>
            <div className="export-buttons">
              <button onClick={() => handleExport('csv')} className="btn-export">
                📄 Export CSV
              </button>
              <button onClick={() => handleExport('excel')} className="btn-export">
                📊 Export Excel
              </button>
            </div>
          </div>
        </div>

        <div className="table-container">
          <table className="results-table">
            <thead>
              <tr>
                {Object.keys(sampleResults[0]).map((header, index) => (
                  <th key={index}>{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sampleResults.map((row, index) => (
                <tr key={index} className={index === 0 ? 'high-risk' : ''}>
                  {Object.values(row).map((cell, cellIndex) => (
                    <td key={cellIndex}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Narrative Analysis */}
      <div className="narrative-section">
        <h4>📝 Analysis Narrative (Generated in 1.9s)</h4>
        <div className="narrative-content">
          <pre>{sampleNarrative}</pre>
        </div>
      </div>

      {/* Validation & Quality Information */}
      <div className="validation-section">
        <h4>🔍 Data Quality Assessment</h4>
        <div className="validation-warnings">
          {sampleWarnings.map((warning, index) => (
            <div key={index} className={`warning-item ${warning.type}`}>
              {warning.message}
            </div>
          ))}
        </div>
        
        <div className="quality-metrics">
          <div className="quality-grid">
            <div className="quality-item">
              <span className="quality-label">Data Quality Score:</span>
              <span className="quality-value">95/100 ⭐⭐⭐⭐⭐</span>
            </div>
            <div className="quality-item">
              <span className="quality-label">Records Processed:</span>
              <span className="quality-value">3 records</span>
            </div>
            <div className="quality-item">
              <span className="quality-label">Processing Time:</span>
              <span className="quality-value">11.2s (Fast)</span>
            </div>
            <div className="quality-item">
              <span className="quality-label">Context Impact:</span>
              <span className="quality-value">+4,780 tokens</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// CSS STYLES (inline for completeness)
// ============================================================================
// Note: In production, these would be in separate CSS files
const styles = `
.ai-agent-dashboard {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f7fa;
  min-height: 100vh;
  color: #333;
}

.session-header {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 3px solid #4a90e2;
}

.session-header h1 {
  margin: 0;
  color: #4a90e2;
  font-size: 1.5rem;
}

.session-details {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.context-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.context-bar {
  width: 200px;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.context-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.context-fill.normal {
  background: linear-gradient(90deg, #4caf50, #8bc34a);
}

.context-fill.warning {
  background: linear-gradient(90deg, #ff9800, #f44336);
}

.session-controls {
  display: flex;
  gap: 1rem;
}

.btn-optimize, .btn-new-chat {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-optimize {
  background: #2196f3;
  color: white;
}

.btn-new-chat {
  background: #4caf50;
  color: white;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.left-panel, .right-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Component styling */
.context-usage-meter, .process-monitor, .performance-analytics, 
.fallback-tracker, .query-interface, .results-display {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #4a90e2;
}

.context-usage-meter h3, .process-monitor h3, .performance-analytics h3,
.fallback-tracker h3, .query-interface h3, .results-display h3 {
  margin: 0 0 1rem 0;
  color: #4a90e2;
  font-size: 1.2rem;
}

/* Progress bars and indicators */
.usage-bar-container, .progress-bar {
  position: relative;
  background: #e0e0e0;
  border-radius: 10px;
  height: 24px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.usage-bar, .progress-fill {
  height: 100%;
  transition: width 0.5s ease;
  border-radius: 10px;
}

.usage-bar.normal, .progress-fill {
  background: linear-gradient(90deg, #4caf50, #8bc34a);
}

.usage-bar.warning {
  background: linear-gradient(90deg, #ff9800, #ffc107);
}

.usage-bar.critical {
  background: linear-gradient(90deg, #f44336, #ff5722);
}

/* Workflow steps */
.workflow-step {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  border-left: 4px solid transparent;
  transition: all 0.3s ease;
}

.workflow-step.step-completed {
  background: #f1f8e9;
  border-left-color: #4caf50;
}

.workflow-step.step-in_progress {
  background: #e3f2fd;
  border-left-color: #2196f3;
}

.workflow-step.step-pending {
  background: #f5f5f5;
  border-left-color: #9e9e9e;
}

.workflow-step.step-failed {
  background: #ffebee;
  border-left-color: #f44336;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.step-duration {
  margin-left: auto;
  font-size: 0.85rem;
  color: #666;
}

/* Data table */
.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.results-table th {
  background: #f8f9fa;
  padding: 0.75rem;
  text-align: left;
  border-bottom: 2px solid #dee2e6;
  font-weight: 600;
  color: #495057;
}

.results-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #dee2e6;
}

.results-table tr.high-risk {
  background: #fff3cd;
}

.results-table tr:hover {
  background: #f8f9fa;
}

/* Summary cards */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.summary-card.highlight {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.summary-card.warning {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  color: #333;
}

.card-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.card-label {
  font-size: 0.85rem;
  opacity: 0.9;
}

/* Query interface */
.query-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.query-input:focus {
  outline: none;
  border-color: #4a90e2;
}

.query-submit {
  margin-top: 1rem;
  width: 100%;
  padding: 0.75rem;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.query-submit:hover:not(:disabled) {
  background: #357abd;
  transform: translateY(-1px);
}

.query-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Suggestions and history */
.suggestion-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.suggestion-btn {
  padding: 0.5rem 1rem;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.suggestion-btn:hover {
  background: #e9ecef;
  border-color: #4a90e2;
}

/* Responsive design */
@media (max-width: 1200px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .session-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .dashboard-content {
    padding: 1rem;
  }
  
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
`;

// ============================================================================
// EXPORT AND SETUP
// ============================================================================
export default AIAgentDashboard;

// Add styles to document head (in real app, would be in CSS file)
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  document.head.appendChild(styleSheet);
}