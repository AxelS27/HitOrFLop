

const Navbar = ({ activePage, setActivePage }: { activePage: string, setActivePage: (page: string) => void }) => {
  return (
    <nav style={{ 
      background: 'rgba(0, 0, 0, 0.85)', 
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(255,255,255,0.1)', 
      padding: '1.25rem 2rem' 
    }}>
      <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
        <div className="logo cursor-pointer" onClick={() => setActivePage('home')} style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div style={{ fontSize: '1.2rem', fontWeight: 700, letterSpacing: '2px', whiteSpace: 'nowrap' }}>
            HIT OR <span style={{ color: 'var(--theme-color, var(--brand-green))' }}>FLOP?</span>
          </div>
          <div style={{ width: '1px', height: '20px', background: 'rgba(255,255,255,0.1)' }}></div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 400, letterSpacing: '0.5px', textTransform: 'none', lineHeight: 1.2 }}>
            Benchmarking Traditional ML Models <br /> for Music Success Prediction
          </div>
        </div>
        
        <ul className="nav-links" style={{ flex: 2, justifyContent: 'center' }}>
          <li className={activePage === 'home' ? 'active' : ''}>
            <button onClick={() => setActivePage('home')}>Home</button>
          </li>
          <li className={activePage === 'models' ? 'active' : ''}>
            <button onClick={() => setActivePage('models')}>Models</button>
          </li>
          <li className={activePage === 'about' ? 'active' : ''}>
            <button onClick={() => setActivePage('about')}>About</button>
          </li>
        </ul>

        <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
          <a 
            href="https://github.com/AxelS27/MachineLearning" 
            target="_blank" 
            style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '12px',
              textDecoration: 'none',
              color: 'white',
              opacity: 0.8,
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              padding: '8px 16px',
              borderRadius: '8px',
              background: 'rgba(255,255,255,0.06)'
            }}
            onMouseOver={(e: any) => { 
                e.currentTarget.style.opacity = '1'; 
                e.currentTarget.style.color = 'var(--theme-color)';
                e.currentTarget.style.background = 'rgba(255,255,255,0.07)';
            }}
            onMouseOut={(e: any) => { 
                e.currentTarget.style.opacity = '0.5'; 
                e.currentTarget.style.color = 'white';
                e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
            }}
          >
            <span style={{ 
              fontSize: '0.7rem', 
              letterSpacing: '2px', 
              fontWeight: 800,
              textTransform: 'uppercase'
            }}>Source</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
            </svg>
          </a>
        </div>
      </div>

      <style>{`
        .nav-links button {
          background: none;
          border: none;
          color: var(--text-dim);
          text-transform: uppercase;
          font-size: 0.8rem;
          font-weight: 600;
          letter-spacing: 1px;
          cursor: pointer;
          transition: color 0.2s;
        }
        .nav-links button:hover {
          color: white;
        }
        .nav-links .active button {
          color: var(--theme-color, var(--brand-green));
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
