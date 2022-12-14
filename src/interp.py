import numpy as np
from numba import njit, jit


from mesh import Mesh


class NS_x(object):
    """
    """
    def __init__(self, model) -> None:
        self.model = model
        
    
    def _wuds(self,u, rho, gamma, delta):

            Pe = rho*u*delta / gamma
            alfa = Pe*np.abs(Pe) / (10 + 2*Pe**2)
            beta = (1 + 0.005*Pe**2) / (1 + 0.05*Pe**2)

            return alfa, beta
        
    
    def internal(self, id: int, u, v, p):
        """
        Ap*uP = Aw*uW + Ae*uE + As*uS + An*uN + Lp + B

        Return:
            [Ap, Aw, Ae, As, An, Lp, B]
        """

        rho = self.model['rho']
        gamma = self.model['gamma']
        deltax = self.model['deltax']
        deltay = self.model['deltay']
        nx = self.model['unx']
        vnx = self.model['vnx']

        ## Index mapping
        # u : centered
        P0 = id
        W0 = int(id - 1)
        E0 = int(id + 1)
        uW0 = u[W0]
        uP0 = u[P0]
        uE0 = u[E0]

        # v : staggered
        line = id // nx
        P0 = int(id + line)
        E0 = P0 + 1
        S0 = P0 - vnx
        SE0 = S0 + 1

        vP0 = v[P0]
        vE0 = v[E0]
        vS0 = v[S0]
        vSE0 = v[SE0]

        fw = rho*deltay*(uW0 + uP0) / 2
        fe = rho*deltay*(uE0 + uP0) / 2
        fs = rho*deltax*(vS0 + vSE0) / 2
        fn = rho*deltax*(vE0 + vP0) / 2

        dx = gamma*deltay / deltax
        dy = gamma*deltax / deltay

        Lp = 0   

        ## WUDS
        alfaw, betaw = self._wuds((uW0 + uP0) / 2, rho, gamma, deltax)
        alfae, betae = self._wuds((uE0 + uP0) / 2, rho, gamma, deltax)
        alfas, betas = self._wuds((vS0 + vSE0) / 2, rho, gamma, deltay)
        alfan, betan = self._wuds((vE0 + vP0) / 2, rho, gamma, deltay)

        Aw =  (0.5 + alfaw)*fw + betaw*dx
        Ae = -(0.5 - alfae)*fe + betae*dx
        As =  (0.5 + alfas)*fs + betas*dy
        An = -(0.5 - alfan)*fn + betan*dy
        Ap = Aw + Ae + As + An

        return np.array([Ap, Aw, Ae, As, An, Lp, 0])


    def boundary(self, id: int, face, tf, u, v, p):
        """
        Return:
            [Ap, Aw, Ae, As, An, Lp, B]
        """
        rho = self.model['rho']
        gamma = self.model['gamma']
        deltax = self.model['deltax']
        deltay = self.model['deltay']
        nx = self.model['unx']
        vnx = self.model['vnx']
      
        A =  np.zeros(6)
        A[-1] = tf  # B

        # [Ap, Aw, Ae, As, An, Lp, B]
        # [0,  1,  2,  3,  4,  5,  6]
        line = id // nx
        P0 = int(id + line)
        E0 = int(P0 + 1)
        S0 = P0 - vnx
        SE0 = int(S0 + 1)
        
        if face =='W':
            A[0] = 1

        if face =='E':
            A[0] = 1
            
        if face =='S':
                       
            vP0 = v[P0]
            vE0 = v[E0]

            alfan, betan = self._wuds((vE0 + vP0) / 2, rho, gamma, deltay)

            A[0] = 0.5 + alfan  # Ap
            A[4] = -0.5 + alfan  # An

        if face =='N':

            vS0 = v[S0]
            vSE0 = v[SE0]

            alfas, betas = self._wuds((vS0 + vSE0) / 2, rho, gamma, deltay)

            A[0] = 0.5 + alfas  # Ap
            A[3] = -0.5 + alfas  # As

        return A

################################################################################
# V ############################################################################
class NS_y(object):
    """
    """
    def __init__(self, model) -> None:
        self.model = model
        

    def _wuds(self,u, rho, gamma, delta):

            Pe = rho*u*delta / gamma
            alfa = Pe*np.abs(Pe) / (10 + 2*Pe**2)
            beta = (1 + 0.005*Pe**2) / (1 + 0.05*Pe**2)

            return alfa, beta
        
    
    def internal(self, id: int, u, v, p):
        """
        Ap*uP = Aw*uW + Ae*uE + As*uS + An*uN + Lp + B

        Return:
            [Ap, Aw, Ae, As, An, Lp, B]
        """
    

        rho = self.model['rho']
        gamma = self.model['gamma']
        deltax = self.model['deltax']
        deltay = self.model['deltay']
        nx = self.model['vnx']
        unx = self.model['unx']

        ## Index mapping
        # u : centered
        P0 = id
        S0 = int(id - nx)#
        N0 = int(id + nx)

        vS0 = v[S0]
        vP0 = v[P0]
        vN0 = v[N0]

        # v : staggered
        line = id // nx
        P0 = int(id - line) 
        W0 = P0 - 1
        N0 = P0 + unx 
        NW0 = N0 - 1  

        uP0 = u[P0]
        uW0 = u[W0]
        uN0 = u[N0]
        uNW0 = u[NW0]

  
        
        fw = rho*deltay*(uW0 + uNW0) / 2
        fe = rho*deltay*(uP0 + uN0) / 2
        fs = rho*deltax*(vP0 + vS0) / 2
        fn = rho*deltax*(vP0 + vN0) / 2

        dx = gamma*deltay / deltax
        dy = gamma*deltax / deltay

        Lp = 0#-deltax*(pN0 - pP0)

        ## WUDS
        alfaw, betaw = self._wuds((uW0 + uNW0) / 2, rho, gamma, deltax)
        alfae, betae = self._wuds((uP0 + uN0) / 2, rho, gamma, deltax)
        alfas, betas = self._wuds((vP0 + vS0) / 2, rho, gamma, deltax)
        alfan, betan = self._wuds((vP0 + vN0) / 2, rho, gamma, deltax)


        Aw =  (0.5 + alfaw)*fw + betaw*dx
        Ae = -(0.5 - alfae)*fe + betae*dx
        As =  (0.5 + alfas)*fs + betas*dy
        An = -(0.5 - alfan)*fn + betan*dy
        Ap = Aw + Ae + As + An

        return np.array([Ap, Aw, Ae, As, An, Lp, 0])


    def boundary(self, id: int, face, tf, u, v, p):
        """
        """
        #u = self.model['u']
        #v = self.model['v']
        rho = self.model['rho']
        gamma = self.model['gamma']
        deltax = self.model['deltax']
        deltay = self.model['deltay']
        nx = self.model['vnx']
        unx = self.model['unx']

        A =  np.zeros(6)
        A[-1] = tf  # B

        # [Ap, Aw, Ae, As, An, Lp, B]
        # [0,  1,  2,  3,  4,  5,  6]
        # v : staggered
        line = id // nx
        P0 = int(id - line) 
        W0 = P0 - 1 
        N0 = P0 + unx 
        NW0 = N0 - 1  

        if face =='W':
            uP0 = u[P0]
            uN0 = u[N0]

            alfae, betae = self._wuds((uP0 + uN0) / 2, rho, gamma, deltax)

            A[0] = -0.5 + alfae
            A[2] = 0.5 + alfae

        if face =='E':

            uW0 = u[W0]
            uNW0 = u[NW0]
            
            alfaw, betaw = self._wuds((uW0 + uNW0) / 2, rho, gamma, deltax)
            
            A[0] = 0.5 + alfaw  # Ap
            A[1] = -0.5 + alfaw  # Aw
            
        if face =='S':
            A[0] = 1

        if face =='N':
            A[0] = 1


        return A