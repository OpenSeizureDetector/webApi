<!-- File: src/Template/Categories/index.ctp -->

<h1>Categories</h1>
<table>
    <tr>
        <th>Title</th>
        <th>Created</th>
    </tr>

    <?php foreach ($categories as $category): ?>
    <tr>
        <td>
            <?= $category->title ?>
        </td>
        <td>
            <?= $category->created->format(DATE_RFC850) ?>
        </td>
    </tr>
    <?php endforeach; ?>
</table>