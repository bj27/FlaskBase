from controller.core.PROGRESSController import PROGRESSController
class UserController():
    def getUserById( self ):
        response = self.execute(" query ")
        return response


    def execute( self, query = "", commit = False, call = False ):
        progress = PROGRESSController()
        progress.generateInstance()
        content = progress.execute(query, True)
        if commit:  progress.commit()
        self.error = progress.error
        if not content:
            content = []
        progress.close()
        return content