<?php
// src/Controller/CategoriesController.php

namespace App\Controller;

class CategoriesController extends AppController
{
    public function index()
    {
        $this->loadComponent('Paginator');
        $categories = $this->Paginator->paginate($this->Categories->find());
        $this->set(compact('categories'));
    }

    public function view($slug = null)
    {   
	$article = $this->Articles->findAll()->firstOrFail();
    	$this->set(compact('category'));
    }
}