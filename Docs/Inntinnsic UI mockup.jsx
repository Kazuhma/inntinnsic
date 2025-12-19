import React, { useState } from 'react';

const InntinnsicMAUIRedesign = () => {
  const [currentView, setCurrentView] = useState('main');
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [scannedCount, setScannedCount] = useState(0);
  const [flaggedCount, setFlaggedCount] = useState(0);
  const [sensitivity, setSensitivity] = useState(0.6);
  
  const folders = [
    'C:\\Users\\Kazhuma\\Downloads',
    'C:\\Users\\Kazhuma\\Pictures',
    'C:\\Users\\Kazhuma\\Documents',
    'C:\\Users\\Kazhuma\\Desktop',
  ];

  // Simulate scanning
  React.useEffect(() => {
    if (isScanning && progress < 100) {
      const timer = setTimeout(() => {
        setProgress(p => Math.min(p + 0.5, 100));
        setScannedCount(s => s + Math.floor(Math.random() * 8));
        if (Math.random() > 0.95) setFlaggedCount(f => f + 1);
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [isScanning, progress]);

  const startScan = () => {
    setIsScanning(true);
    setProgress(0);
    setScannedCount(0);
    setFlaggedCount(0);
  };

  const stopScan = () => setIsScanning(false);

  const styles = {
    // Color palette
    colors: {
      bgDarkest: '#0F172A',
      bgCard: '#1E293B',
      bgInput: '#0F172A',
      border: '#334155',
      primary: '#3B82F6',
      primaryHover: '#2563EB',
      header: '#2563EB',
      textPrimary: '#FFFFFF',
      textSecondary: '#94A3B8',
      textMuted: '#64748B',
      textLink: '#60A5FA',
      success: '#10B981',
      warning: '#F59E0B',
      danger: '#EF4444',
    }
  };

  if (currentView === 'settings') {
    return <SettingsPage 
      onBack={() => setCurrentView('main')} 
      sensitivity={sensitivity}
      setSensitivity={setSensitivity}
      styles={styles} 
    />;
  }

  return (
    <div style={{
      fontFamily: '"Segoe UI Variable", "Segoe UI", system-ui, sans-serif',
      background: styles.colors.bgDarkest,
      minHeight: '100vh',
      color: styles.colors.textPrimary,
    }}>
      {/* Window Chrome */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        padding: '8px 12px',
        background: '#1a1a2e',
        borderBottom: '1px solid #2d2d44',
      }}>
        <span style={{ fontSize: '13px', color: '#888' }}>Inntinnsic</span>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
          {['−', '□', '×'].map((s, i) => (
            <button key={i} style={{
              width: '36px', height: '28px', border: 'none',
              background: 'transparent', color: '#888', cursor: 'pointer',
              borderRadius: '4px', fontSize: '14px',
            }}>{s}</button>
          ))}
        </div>
      </div>

      {/* Blue Header */}
      <div style={{
        background: styles.colors.header,
        padding: '14px 20px',
        fontSize: '18px',
        fontWeight: '600',
      }}>
        Inntinnsic
      </div>

      {/* Main Content */}
      <div style={{ padding: '20px' }}>
        {/* App Title Card */}
        <div style={{
          background: styles.colors.bgCard,
          borderRadius: '12px',
          border: `1px solid ${styles.colors.border}`,
          padding: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
          marginBottom: '16px',
        }}>
          <div style={{
            width: '48px', height: '48px', borderRadius: '12px',
            background: 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '24px',
          }}>🛡️</div>
          <div>
            <h1 style={{ margin: 0, fontSize: '22px', fontWeight: '600' }}>Image Safety Checker</h1>
            <p style={{ margin: '4px 0 0 0', color: styles.colors.textSecondary, fontSize: '14px' }}>
              Scan your computer for potentially inappropriate images
            </p>
          </div>
        </div>

        {/* Action Buttons Row - REDESIGNED */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 44px',
          gap: '12px',
          marginBottom: '16px',
        }}>
          <button style={{
            padding: '12px 16px',
            background: styles.colors.bgCard,
            border: `1px solid ${styles.colors.border}`,
            borderRadius: '8px',
            color: 'white',
            fontSize: '14px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
          }}>
            📁 Add Folder
          </button>
          <button style={{
            padding: '12px 20px',
            background: styles.colors.primary,
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
          }}>
            ⚡ Quick Scan
          </button>
          <button 
            onClick={() => setCurrentView('settings')}
            style={{
              padding: '0',
              width: '44px',
              height: '44px',
              background: styles.colors.bgCard,
              border: `1px solid ${styles.colors.border}`,
              borderRadius: '8px',
              color: styles.colors.textSecondary,
              fontSize: '18px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
            ⚙️
          </button>
        </div>

        {/* Selected Folders - REDESIGNED (taller) */}
        <div style={{
          background: styles.colors.bgCard,
          borderRadius: '12px',
          border: `1px solid ${styles.colors.border}`,
          marginBottom: '16px',
          minHeight: '200px',
          maxHeight: '240px',
          display: 'flex',
          flexDirection: 'column',
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '14px 16px',
            borderBottom: `1px solid ${styles.colors.border}`,
          }}>
            <span style={{ fontWeight: '600', fontSize: '14px' }}>Selected Folders</span>
            <button style={{
              padding: '6px 14px',
              background: styles.colors.danger,
              border: 'none',
              borderRadius: '6px',
              color: 'white',
              fontSize: '12px',
              cursor: 'pointer',
            }}>Clear All</button>
          </div>
          <div style={{ flex: 1, overflow: 'auto', padding: '8px' }}>
            {folders.map((folder, i) => (
              <div key={i} style={{
                display: 'flex',
                alignItems: 'center',
                padding: '10px 14px',
                background: styles.colors.bgInput,
                borderRadius: '8px',
                border: `1px solid ${styles.colors.border}`,
                marginBottom: '6px',
              }}>
                <span style={{ marginRight: '12px', fontSize: '16px' }}>📁</span>
                <span style={{
                  flex: 1,
                  fontSize: '13px',
                  color: styles.colors.textSecondary,
                  fontFamily: '"Cascadia Code", "Consolas", monospace',
                }}>{folder}</span>
                <button style={{
                  width: '28px', height: '28px',
                  background: 'transparent',
                  border: 'none',
                  color: styles.colors.danger,
                  cursor: 'pointer',
                  borderRadius: '4px',
                  fontSize: '14px',
                }}>✕</button>
              </div>
            ))}
          </div>
        </div>

        {/* Scan Status - REDESIGNED (fixed height) */}
        <div style={{
          background: isScanning 
            ? 'linear-gradient(135deg, #1E293B 0%, #1E3A5F 100%)'
            : styles.colors.bgCard,
          borderRadius: '12px',
          border: `1px solid ${styles.colors.border}`,
          padding: '16px 20px',
          marginBottom: '16px',
          height: '160px',
          display: 'flex',
          flexDirection: 'column',
        }}>
          {/* Header row with title and View Results button */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>
                {isScanning 
                  ? `Analyzing ${Math.floor(scannedCount / progress * 100) || 6145} Images...`
                  : progress >= 100 
                    ? 'Scan Complete'
                    : 'Ready to Scan'
                }
              </h3>
              <p style={{ margin: '4px 0 0 0', fontSize: '13px', color: styles.colors.textSecondary }}>
                {isScanning 
                  ? `Analyzing: Screenshot 2025-12-08 150136.png (${scannedCount}/6145)`
                  : 'Select folders above to begin scanning'
                }
              </p>
            </div>
            {/* View Results - secondary button, same width as Start Scan */}
            <button style={{
              background: styles.colors.bgCard,
              border: `1px solid ${styles.colors.border}`,
              borderRadius: '8px',
              color: 'white',
              fontSize: '15px',
              fontWeight: '600',
              cursor: 'pointer',
              padding: '14px 0',
              width: '160px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
            }}>
              ⦿ View Results
            </button>
          </div>

          {/* Progress bar */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
          }}>
            <div style={{
              width: '100%',
              height: '6px',
              background: styles.colors.border,
              borderRadius: '3px',
              overflow: 'hidden',
            }}>
              <div style={{
                width: `${progress}%`,
                height: '100%',
                background: `linear-gradient(90deg, ${styles.colors.primary} 0%, #60A5FA 100%)`,
                borderRadius: '3px',
                transition: 'width 0.1s ease',
                boxShadow: isScanning ? '0 0 10px rgba(59, 130, 246, 0.5)' : 'none',
              }} />
            </div>
          </div>

          {/* Action button - same spacing from progress bar as View Results */}
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '12px' }}>
            <button 
              onClick={isScanning ? stopScan : startScan}
              style={{
                padding: '14px 0',
                background: isScanning ? styles.colors.danger : styles.colors.primary,
                border: 'none',
                borderRadius: '8px',
                color: 'white',
                fontSize: '15px',
                fontWeight: '600',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                width: '160px',
              }}>
              {isScanning ? '■ Stop Scan' : '▶ Start Scan'}
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '16px',
        }}>
          <StatCard 
            value={scannedCount}
            label="Images Scanned"
            color={styles.colors.primary}
          />
          <StatCard 
            value={flaggedCount}
            label="Flagged"
            color={styles.colors.warning}
          />
          <StatCard 
            value={isScanning ? 'Scanning' : progress >= 100 ? 'Complete' : 'Ready'}
            label="Status"
            color={styles.colors.success}
            isText
          />
        </div>
      </div>

      {/* Design Annotation */}
      <div style={{
        margin: '20px',
        padding: '16px 20px',
        background: 'rgba(59, 130, 246, 0.1)',
        borderRadius: '8px',
        border: '1px solid rgba(59, 130, 246, 0.2)',
        fontSize: '13px',
        color: styles.colors.textSecondary,
      }}>
        <strong style={{ color: styles.colors.textLink }}>📐 Key Changes:</strong>
        <span style={{ marginLeft: '8px' }}>
          Settings → icon button | Folders section → taller with scroll | Scan status → fixed height (no shift) | View Results → subtle link
        </span>
      </div>
    </div>
  );
};

const StatCard = ({ value, label, color, isText }) => (
  <div style={{
    background: color,
    borderRadius: '12px',
    padding: '16px 20px',
  }}>
    <div style={{ 
      fontSize: isText ? '22px' : '32px', 
      fontWeight: '700',
      color: 'white',
    }}>
      {typeof value === 'number' ? value.toLocaleString() : value}
    </div>
    <div style={{ 
      fontSize: '12px', 
      color: 'rgba(255,255,255,0.8)',
      marginTop: '2px',
    }}>{label}</div>
  </div>
);

const SettingsPage = ({ onBack, sensitivity, setSensitivity, styles }) => {
  const [flags, setFlags] = useState({
    femaleBreast: true,
    femaleGenitalia: true,
    maleGenitalia: true,
    buttocks: true,
    belly: false,
    feet: false,
  });

  const [options, setOptions] = useState({
    autoExport: false,
    skipHidden: true,
    confirmDelete: true,
  });

  const CheckboxItem = ({ label, checked, onChange, compact }) => (
    <div 
      onClick={() => onChange(!checked)}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        padding: compact ? '10px 12px' : '0',
        background: compact ? styles.colors.bgInput : 'transparent',
        borderRadius: compact ? '8px' : '0',
        border: compact ? `1px solid ${styles.colors.border}` : 'none',
        cursor: 'pointer',
      }}>
      <div style={{
        width: '20px',
        height: '20px',
        borderRadius: '4px',
        border: checked ? 'none' : `2px solid ${styles.colors.textMuted}`,
        background: checked ? styles.colors.primary : 'transparent',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexShrink: 0,
      }}>
        {checked && <span style={{ color: 'white', fontSize: '12px' }}>✓</span>}
      </div>
      <span style={{ fontSize: '13px', color: styles.colors.textPrimary }}>{label}</span>
    </div>
  );

  const OptionRow = ({ label, description, checked, onChange }) => (
    <div style={{
      display: 'flex',
      alignItems: 'flex-start',
      gap: '12px',
      padding: '12px 0',
      borderBottom: `1px solid ${styles.colors.border}`,
      cursor: 'pointer',
    }} onClick={() => onChange(!checked)}>
      <div style={{
        width: '20px',
        height: '20px',
        borderRadius: '4px',
        border: checked ? 'none' : `2px solid ${styles.colors.textMuted}`,
        background: checked ? styles.colors.primary : 'transparent',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexShrink: 0,
        marginTop: '2px',
      }}>
        {checked && <span style={{ color: 'white', fontSize: '12px' }}>✓</span>}
      </div>
      <div>
        <div style={{ fontSize: '14px', color: styles.colors.textPrimary }}>{label}</div>
        <div style={{ fontSize: '12px', color: styles.colors.textMuted, marginTop: '2px' }}>{description}</div>
      </div>
    </div>
  );

  return (
    <div style={{
      fontFamily: '"Segoe UI Variable", "Segoe UI", system-ui, sans-serif',
      background: styles.colors.bgDarkest,
      minHeight: '100vh',
      color: styles.colors.textPrimary,
    }}>
      {/* Window Chrome */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        padding: '8px 12px',
        background: '#1a1a2e',
        borderBottom: '1px solid #2d2d44',
      }}>
        <span style={{ fontSize: '13px', color: '#888' }}>Inntinnsic</span>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
          {['−', '□', '×'].map((s, i) => (
            <button key={i} style={{
              width: '36px', height: '28px', border: 'none',
              background: 'transparent', color: '#888', cursor: 'pointer',
              borderRadius: '4px', fontSize: '14px',
            }}>{s}</button>
          ))}
        </div>
      </div>

      {/* Blue Header with Back Button */}
      <div style={{
        background: styles.colors.header,
        padding: '14px 20px',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
      }}>
        <button 
          onClick={onBack}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'white',
            fontSize: '20px',
            cursor: 'pointer',
            padding: '4px 8px',
          }}>←</button>
        <span style={{ fontSize: '18px', fontWeight: '600' }}>Settings</span>
      </div>

      {/* Scrollable Content */}
      <div style={{ padding: '20px', maxHeight: 'calc(100vh - 120px)', overflow: 'auto' }}>
        
        {/* Detection Sensitivity */}
        <div style={{
          background: styles.colors.bgCard,
          borderRadius: '12px',
          border: `1px solid ${styles.colors.border}`,
          padding: '20px',
          marginBottom: '16px',
        }}>
          <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: '600' }}>
            Detection Sensitivity
          </h3>
          <p style={{ margin: '0 0 16px 0', fontSize: '13px', color: styles.colors.textSecondary }}>
            Higher values = more strict detection (fewer false positives)
          </p>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '12px', color: styles.colors.textMuted }}>Low</span>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.01"
              value={sensitivity}
              onChange={(e) => setSensitivity(parseFloat(e.target.value))}
              style={{ flex: 1, accentColor: styles.colors.primary }}
            />
            <span style={{ fontSize: '12px', color: styles.colors.textMuted }}>High</span>
          </div>
          
          <div style={{ 
            textAlign: 'center', 
            marginTop: '12px',
            color: styles.colors.textLink,
            fontSize: '14px',
          }}>
            Current: {sensitivity.toFixed(2)}
          </div>
        </div>

        {/* Content to Flag */}
        <div style={{
          background: styles.colors.bgCard,
          borderRadius: '12px',
          border: `1px solid ${styles.colors.border}`,
          padding: '20px',
          marginBottom: '16px',
        }}>
          <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', fontWeight: '600' }}>
            Content to Flag
          </h3>
          <p style={{ margin: '0 0 16px 0', fontSize: '13px', color: styles.colors.textSecondary }}>
            Select which content types should trigger a flag
          </p>
          
          {/* 2-column grid */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '10px',
          }}>
            <CheckboxItem 
              label="Female Breast Exposed" 
              checked={flags.femaleBreast}
              onChange={(v) => setFlags({...flags, femaleBreast: v})}
              compact
            />
            <CheckboxItem 
              label="Female Genitalia Exposed" 
              checked={flags.femaleGenitalia}
              onChange={(v) => setFlags({...flags, femaleGenitalia: v})}
              compact
            />
            <CheckboxItem 
              label="Male Genitalia Exposed" 
              checked={flags.maleGenitalia}
              onChange={(v) => setFlags({...flags, maleGenitalia: v})}
              compact
            />
            <CheckboxItem 
              label="Buttocks Exposed" 
              checked={flags.buttocks}
              onChange={(v) => setFlags({...flags, buttocks: v})}
              compact
            />
            <CheckboxItem 
              label="Belly Exposed" 
              checked={flags.belly}
              onChange={(v) => setFlags({...flags, belly: v})}
              compact
            />
            <CheckboxItem 
              label="Feet Exposed" 
              checked={flags.feet}
              onChange={(v) => setFlags({...flags, feet: v})}
              compact
            />
          </div>

          {/* Info note */}
          <div style={{
            marginTop: '16px',
            padding: '10px 14px',
            background: 'rgba(59, 130, 246, 0.15)',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <span>ℹ️</span>
            <span style={{ fontSize: '12px', color: '#93C5FD', fontStyle: 'italic' }}>
              Note: Anus Exposed is always flagged
            </span>
          </div>
        </div>

        {/* Scan Options */}
        <div style={{
          background: styles.colors.bgCard,
          borderRadius: '12px',
          border: `1px solid ${styles.colors.border}`,
          padding: '20px',
          marginBottom: '16px',
        }}>
          <h3 style={{ margin: '0 0 16px 0', fontSize: '16px', fontWeight: '600' }}>
            Scan Options
          </h3>
          
          <OptionRow 
            label="Auto Export Results"
            description="Automatically save scan results to a file"
            checked={options.autoExport}
            onChange={(v) => setOptions({...options, autoExport: v})}
          />
          <OptionRow 
            label="Skip Hidden Files"
            description="Don't scan files with hidden attribute"
            checked={options.skipHidden}
            onChange={(v) => setOptions({...options, skipHidden: v})}
          />
          <div style={{ borderBottom: 'none' }}>
            <OptionRow 
              label="Confirm File Deletions"
              description="Ask for confirmation before deleting files"
              checked={options.confirmDelete}
              onChange={(v) => setOptions({...options, confirmDelete: v})}
            />
          </div>
        </div>

        {/* Action Buttons - no icons, self-explanatory */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '16px',
          marginBottom: '20px',
        }}>
          <button style={{
            padding: '14px 20px',
            background: '#374151',
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            fontSize: '14px',
            cursor: 'pointer',
          }}>
            Reset to Defaults
          </button>
          <button style={{
            padding: '14px 20px',
            background: styles.colors.primary,
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
          }}>
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
};

export default InntinnsicMAUIRedesign;
