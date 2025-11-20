
import './globals.css';

.

export const metadata = {

  title: 'SideGuy Solutions | Where Code Meets the Coastline',

  description:

    'SideGuy Solutions — coastal tech concierge for apps, automation, and Web3 in San Diego.'

};



export default function RootLayout({ children }) {

  return (

    <html lang="en">

      <body style={{ margin: 0, backgroundColor: '#020617', color: 'white' }}>

        {children}

      </body>

    </html>

  );

}
