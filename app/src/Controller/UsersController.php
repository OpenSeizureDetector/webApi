<?php
namespace App\Controller;

use App\Controller\AppController;
use Cake\Event\Event;

/**
 * Users Controller
 *
 * @property \App\Model\Table\UsersTable $Users
 *
 * @method \App\Model\Entity\User[]|\Cake\Datasource\ResultSetInterface paginate($object = null, array $settings = [])
 */
class UsersController extends AppController
{
    public function beforeFilter(Event $event)
    {	
        parent::beforeFilter($event);
        //$this->Authentication->allowUnauthenticated(['index']);
        $result = $this->Authentication->getResult();
        if (!$result->isValid()) {
            echo "index(): Authentication failed\n";
            print_r($result->getData());
            print_r($result->getErrors());
            $response = $this->response->withStatus(403);
            return $response;            
        } else {
            //echo("beforeFilter() - Authenticated ok");
        }
    }
    
    /**
     * Index method
     *
     * @return \Cake\Http\Response|null
     */
    public function index()
    {
        $this->loadComponent('Paginator');
        $user = $this->request->getAttribute('identity');
        $query = $user->applyScope('index', $this->Users->find());
        $users = $this->Paginator->paginate($query);
        
        $this->set(compact('users'));
        $this->set('_serialize', ['users']);        
    }

    /**
     * View method
     *
     * @param string|null $id User id.
     * @return \Cake\Http\Response|null
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function view($id = null)
    {
        //echo("Retrieving Record for User ".$id);
        $userrec = $this->Users->get($id, [
            'contain' => ['Usertypes']
        ]);
        $this->Authorization->authorize($userrec);


        $this->set('user', $userrec);
        $this->set('_serialize',['user']);
    }

    /**
     * Add method
     *
     * @return \Cake\Http\Response|null Redirects on successful add, renders view otherwise.
     */
    public function add()
    {
        $this->request->allowMethod(['post', 'put']);
        $userrec = $this->Users->newEntity($this->request->getData());
        $this->Authorization->authorize($userrec,'create');
        if ($this->Users->save($userrec)) {
            $msg = 'Success';
        } else {
            $msg = 'Failed';
        }
        $this->set([
            'msg' => $msg,
            'user' => $userrec,
            '_serialize' => ['msg', 'user']
        ]);

/*        $user = $this->Users->newEntity();
        $this->Authorization->authorize($user,'create');

        if ($this->request->is('post')) {
            $user = $this->Users->patchEntity($user, $this->request->getData());
            echo("add");
            echo(print_r($this->request->getData()));
            if ($this->Users->save($user)) {
                $this->Flash->success(__('The user has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The user could not be saved. Please, try again.'));
        }
        $usertypes = $this->Users->Usertypes->find('list', ['limit' => 200]);
        $this->set(compact('user', 'usertypes'));
        $this->set('_serialize',['user']);
*/
    }

    /**
     * Edit method
     *
     * @param string|null $id User id.
     * @return \Cake\Http\Response|null Redirects on successful edit, renders view otherwise.
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function edit($id = null)
    {
        $user = $this->Users->get($id, [
            'contain' => []
        ]);
        $this->Authorization->authorize($user,'update');
        if ($this->request->is(['patch', 'post', 'put'])) {
            $user = $this->Users->patchEntity($user, $this->request->getData());
            if ($this->Users->save($user)) {
                $msg="Success";
            } else {
                $msg="Failed";
            }
        }
        $usertypes = $this->Users->Usertypes->find('list', ['limit' => 200]);
        $this->set(compact('msg','user', 'usertypes'));
        $this->set('_serialize',['msg']);
    }

    /**
     * Delete method
     *
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $user = $this->Users->get($id);
        $this->Authorization->authorize($user,'delete');
        if ($this->Users->delete($user)) {
            $msg="Success";
        } else {
            $msg="Failed";
        }

        $this->set('_serialize',['msg']);
    }
}
