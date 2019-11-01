<?php
namespace App\Controller;

use App\Controller\AppController;

/**
 * Usertypes Controller
 *
 *
 * @method \App\Model\Entity\Usertype[]|\Cake\Datasource\ResultSetInterface paginate($object = null, array $settings = [])
 */
class UsertypesController extends AppController
{
    /**
     * Index method
     *
     * @return \Cake\Http\Response|null
     */
    public function index()
    {
        $usertypes = $this->paginate($this->Usertypes);

        $this->set(compact('usertypes'));
    }

    /**
     * View method
     *
     * @param string|null $id Usertype id.
     * @return \Cake\Http\Response|null
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function view($id = null)
    {
        $usertype = $this->Usertypes->get($id, [
            'contain' => []
        ]);

        $this->set('usertype', $usertype);
    }

    /**
     * Add method
     *
     * @return \Cake\Http\Response|null Redirects on successful add, renders view otherwise.
     */
    public function add()
    {
        $usertype = $this->Usertypes->newEntity();
        if ($this->request->is('post')) {
            $usertype = $this->Usertypes->patchEntity($usertype, $this->request->getData());
            if ($this->Usertypes->save($usertype)) {
                $this->Flash->success(__('The usertype has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The usertype could not be saved. Please, try again.'));
        }
        $this->set(compact('usertype'));
    }

    /**
     * Edit method
     *
     * @param string|null $id Usertype id.
     * @return \Cake\Http\Response|null Redirects on successful edit, renders view otherwise.
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function edit($id = null)
    {
        $usertype = $this->Usertypes->get($id, [
            'contain' => []
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            $usertype = $this->Usertypes->patchEntity($usertype, $this->request->getData());
            if ($this->Usertypes->save($usertype)) {
                $this->Flash->success(__('The usertype has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The usertype could not be saved. Please, try again.'));
        }
        $this->set(compact('usertype'));
    }

    /**
     * Delete method
     *
     * @param string|null $id Usertype id.
     * @return \Cake\Http\Response|null Redirects to index.
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $usertype = $this->Usertypes->get($id);
        if ($this->Usertypes->delete($usertype)) {
            $this->Flash->success(__('The usertype has been deleted.'));
        } else {
            $this->Flash->error(__('The usertype could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'index']);
    }
}
