

const Navbar = ({ activePage, setActivePage }: { activePage: string, setActivePage: (page: string) => void }) => {
  return (
    <nav style={{ background: '#000000', borderBottom: '1px solid rgba(255,255,255,0.05)', padding: '1.25rem 2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
        <div className="logo cursor-pointer" onClick={() => setActivePage('home')} style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div style={{ fontSize: '1.2rem', fontWeight: 700, letterSpacing: '2px', whiteSpace: 'nowrap' }}>
            HIT OR <span style={{ color: 'var(--brand-green)' }}>FLOP?</span>
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

        <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
          <button className="btn-primary" style={{ padding: '0.6rem 1.5rem', fontSize: '0.8rem' }}>
            CREDITS
          </button>
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
          color: var(--brand-green);
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
