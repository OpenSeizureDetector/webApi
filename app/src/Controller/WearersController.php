<?php
namespace App\Controller;

use App\Controller\AppController;
use Cake\Event\Event;

/**
 * Wearers Controller
 *
 * @property \App\Model\Table\WearersTable $Wearers
 *
 * @method \App\Model\Entity\Wearer[]|\Cake\Datasource\ResultSetInterface paginate($object = null, array $settings = [])
 */
class WearersController extends AppController
{
    public function beforeFilter(Event $event)
    {	
        parent::beforeFilter($event);
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
    
    
    public function index()
    {
        $user = $this->request->getAttribute('identity');
        $query = $user->applyScope('index', $this->Wearers->find());
        $wearers = $this->paginate($query);

        $this->set(compact('wearers'));
        $this->set('_serialize', ['wearers']);        
    }

    /**
     * View method
     *
     * @param string|null $id Wearer id.
     * @return \Cake\Http\Response|null
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function view($id = null)
    {
        $wearer = $this->Wearers->get($id);
        $this->Authorization->authorize($wearer);

        $this->set('wearer', $wearer);
        $this->set('_serialize',['wearer']);
    }

    /**
     * Add method
     *
     * @return \Cake\Http\Response|null Redirects on successful add, renders view otherwise.
     */
    public function add()
    {
        $this->request->allowMethod(['post', 'put']);
        $wearer = $this->Wearers->newEntity($this->request->getData());
        $this->Authorization->authorize($wearer,'create');
        if ($this->Wearers->save($wearer)) {
            $msg = "Success";
        } else {
            $msg = "Failed";
        }
        $this->set([
            'msg' => $msg,
            'wearer' => $wearer,
            '_serialize' => ['msg', 'wearer']
        ]);
    }

    /**
     * Edit method
     *
     * @param string|null $id Wearer id.
     * @return \Cake\Http\Response|null Redirects on successful edit, renders view otherwise.
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function edit($id = null)
    {
        $wearer = $this->Wearers->get($id, [
            'contain' => []
        ]);
        $this->Authorization->authorize($wearer,'update');

        if ($this->request->is(['patch', 'post', 'put'])) {
            $wearer = $this->Wearers->patchEntity($wearer, $this->request->getData());
            if ($this->Wearers->save($wearer)) {
                $msg = "Success";
            } else {
                $msg = "Failed";
            }
            $this->Flash->error(__('The wearer could not be saved. Please, try again.'));
        }
        $this->set(compact('msg', 'wearer'));
        $this->set('_serialize',['msg']);
    }

    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $wearer = $this->Wearers->get($id);
        $this->Authorization->authorize($wearer,'delete');
        if ($this->Wearers->delete($wearer)) {
            $msg="Success";
        } else {
            $msg="Failed";
        }

        $this->set('_serialize',['msg']);
    }
}
